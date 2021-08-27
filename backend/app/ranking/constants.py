# TODO: Replace these with values from the skill registry

# Overall skill weights
skill_weights = {
    "AVA": 2,
    "HEALTH": 2,
    "Providers": 1,
    "Benefits": 1,
    "OptumRx": 1,
    "Optum Bank": 1,
    "Claims": 1,
}

default_content_weights = {
    "heading_org": 1,
    "content_org": 1,
    "heading_aug": 1,
    "content_aug": 1,
}

# Skill content-specific weights
skill_content_weights = {
    "AVA": {"heading_org": 4, "content_org": 2, "heading_aug": 2, "content_aug": 1},
    "HEALTH": {"heading_org": 4, "content_org": 2, "heading_aug": 2, "content_aug": 1},
    "Providers": default_content_weights,
    "Benefits": default_content_weights,
    "MyUHC": default_content_weights,
    "OptumRx": default_content_weights,
    "Optum Bank": default_content_weights,
    "Claims": default_content_weights,
}

# domain scores weights based on skill
skill_domain_weights = {
    "AVA": 1,
    "HEALTH": 1,
    "Providers": 2,
    "Benefits": 2,
    "OptumRx": 2,
    "Optum Bank": 2,
    "Claims": 2,
}
