modules = {
    "Exotic": {
        "types": {
            "weapons": [
                {
                    "label": "Infraknife Accelerator",
                    "key": "infra",
                    "modules": [
                        {"id": "IK", "type": "core", "label": "Infraknife Accelerator", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "infra.png"},
                        {"id": "QR", "type": "bonus", "label": "Q-Resonator", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "q-resonator.png"},
                        {"id": "Xa", "type": "bonus", "label": "Infra Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Infra Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Infra Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                    ],
                },
                {
                    "label": "Photon Cannon",
                    "key": "photon",
                    "modules": [
                        {"id": "PC", "type": "core", "label": "Photon Cannon", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "photon_core.png"},
                        {"id": "Pa", "type": "bonus", "label": "Photon Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "photon_upgrade_sigma.png"},
                        {"id": "Pb", "type": "bonus", "label": "Photon Upgrade Tau", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "photon_upgrade_tau.png"},
                        {"id": "Pc", "type": "bonus", "label": "Photon Upgrade Theta", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "photon_upgrade_theta.png"},
                    ],
                },
            ],
             "shields": [
                 {
                    "label": "Starship Shields",
                    "key": "shield",
                    "modules": [
                        {"id": "DS", "type": "core", "label": "Defensive Shields", "bonus": 0.0, "adjacency": True, "sc_eligible": True, "image": "shield.png"},
                        {"id": "AA", "type": "bonus", "label": "Ablative Armor", "bonus": 0.07, "adjacency": False, "sc_eligible": False, "image": "ablative.png"},
                        {"id": "Sa", "type": "bonus", "label": "Shield Upgrade Sigma", "bonus": 0.3, "adjacency": True, "sc_eligible": True, "image": "shield-upgrade.png"},
                        {"id": "Sb", "type": "bonus", "label": "Shield Upgrade Tau", "bonus": 0.3, "adjacency": True, "sc_eligible": True, "image": "shield-upgrade.png"},
                        {"id": "Sc", "type": "bonus", "label": "Shield Upgrade Theta", "bonus": 0.3, "adjacency": True, "sc_eligible": True, "image": "shield-upgrade.png"},
                    ],
                 },
            ]
        },
    },
    # Add other ships here if needed (e.g., "Fighter", "Hauler")
}
