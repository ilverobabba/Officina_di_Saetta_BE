from sqlalchemy import select, or_, and_
from model.compatibility import Compatibility, CompatibilityRule


def get_all_rules(session):
    return session.execute(select(CompatibilityRule)).scalars().all()

def get_rule_by_id(session, rule_id):
    return session.get(CompatibilityRule, rule_id)

def save_rule(session, rule):
    session.add(rule)
    session.commit()
    return rule

def delete_rule(session, rule):
    session.delete(rule)
    session.commit()

def get_all_compatibilities(session):
    return session.execute(select(Compatibility)).scalars().all()

def get_between(session, opt_a, opt_b):
    return session.execute(
        select(Compatibility).where(
            or_(
                and_(Compatibility.optional_id == opt_a, Compatibility.optional_with_id == opt_b),
                and_(Compatibility.optional_id == opt_b, Compatibility.optional_with_id == opt_a),
            )
        )
    ).scalars().first()

def get_by_optional(session, optional_id):
    return session.execute(
        select(Compatibility).where(
            or_(Compatibility.optional_id == optional_id, Compatibility.optional_with_id == optional_id)
        )
    ).scalars().all()

def save_compatibility(session, compatibility):
    session.add(compatibility)
    session.commit()
    return compatibility

def delete_compatibility(session, compatibility):
    session.delete(compatibility)
    session.commit()
