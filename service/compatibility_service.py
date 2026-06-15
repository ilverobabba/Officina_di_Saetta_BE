from model.compatibility import Compatibility, CompatibilityRule
from repository import compatibility_repository, optional_repository

RULE_TYPES = ["incompatible", "requires"]


def get_all_rules(session):
    return compatibility_repository.get_all_rules(session)


def create_rule(session, data):
    if data.get("rule_type") not in RULE_TYPES:
        raise ValueError(f"rule_type deve essere uno di: {RULE_TYPES}")
    return compatibility_repository.save_rule(session, CompatibilityRule(rule_type=data["rule_type"]))


def delete_rule(session, rule_id):
    rule = compatibility_repository.get_rule_by_id(session, rule_id)
    if not rule:
        raise ValueError(f"Regola con id={rule_id} non trovata!")
    compatibility_repository.delete_rule(session, rule)


def get_all_compatibilities(session):
    return compatibility_repository.get_all_compatibilities(session)


def create_compatibility(session, data):
    if not all(k in data for k in ["optional_id", "optional_with_id", "rule_id"]):
        raise ValueError("Campi obbligatori: optional_id, optional_with_id, rule_id")

    opt_a = optional_repository.get_by_id(session, int(data["optional_id"]))
    opt_b = optional_repository.get_by_id(session, int(data["optional_with_id"]))
    rule = compatibility_repository.get_rule_by_id(session, int(data["rule_id"]))

    if not opt_a: raise ValueError(f"Optional con id={data['optional_id']} non trovato!")
    if not opt_b: raise ValueError(f"Optional con id={data['optional_with_id']} non trovato!")
    if not rule:  raise ValueError(f"Regola con id={data['rule_id']} non trovata!")
    if opt_a.optional_id == opt_b.optional_id:
        raise ValueError("I due optional non possono essere uguali!")
    if compatibility_repository.get_between(session, opt_a.optional_id, opt_b.optional_id):
        raise ValueError("Esiste già una regola di compatibilità tra questi due optional!")

    return compatibility_repository.save_compatibility(session, Compatibility(
        optional_id=opt_a.optional_id,
        optional_with_id=opt_b.optional_id,
        rule_id=rule.rule_id,
    ))


def delete_compatibility(session, compatibility_id):
    comp = session.get(Compatibility, compatibility_id)
    if not comp:
        raise ValueError(f"Compatibility con id={compatibility_id} non trovata!")
    compatibility_repository.delete_compatibility(session, comp)


def check_optional_list(session, optional_ids):
    """Verifica compatibilità tra optional. Ritorna lista di violazioni (vuota = ok)."""
    violazioni = []

    # Controlla incompatibilità tra coppie
    for i in range(len(optional_ids)):
        for j in range(i + 1, len(optional_ids)):
            comp = compatibility_repository.get_between(session, optional_ids[i], optional_ids[j])
            if comp and comp.rule.rule_type == "incompatible":
                violazioni.append({
                    "optional_id_a": optional_ids[i],
                    "optional_id_b": optional_ids[j],
                    "rule_type": "incompatible",
                    "message": f"Optional {optional_ids[i]} e Optional {optional_ids[j]} sono incompatibili!",
                })

    # Controlla "requires": se A richiede B, B deve essere nella lista
    for opt_id in optional_ids:
        for entry in compatibility_repository.get_by_optional(session, opt_id):
            if entry.rule.rule_type == "requires":
                altro_id = entry.optional_with_id if entry.optional_id == opt_id else entry.optional_id
                if altro_id not in optional_ids:
                    violazioni.append({
                        "optional_id_a": opt_id,
                        "optional_id_b": altro_id,
                        "rule_type": "requires",
                        "message": f"Optional {opt_id} richiede anche l'Optional {altro_id}!",
                    })

    return violazioni
