modules = {
    "Exotic": {
        "types": {
            "weapons": [
                {
                    "label": "Cyclotron Ballista",
                    "key": "cyclotron",
                    "modules": [
                        {"id": "CB", "type": "core", "label": "Cyclotron Ballista", "bonus": 1.0, "adjacency": False, "sc_eligible": True, "image": "cyclotron.png"},
                        {"id": "QR", "type": "bonus", "label": "Dyson Pump", "bonus": 0.1, "adjacency": False, "sc_eligible": True, "image": "dyson.png"},
                        {"id": "Xa", "type": "bonus", "label": "Cyclotron Ballista Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Cyclotron Ballista Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Cyclotron Ballista Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                    ],
                },                
                {
                    "label": "Infraknife Accelerator",
                    "key": "infra",
                    "modules": [
                        {"id": "IK", "type": "core", "label": "Infraknife Accelerator", "bonus": 1.0, "adjacency": False, "sc_eligible": True, "image": "infra.png"},
                        {"id": "QR", "type": "reward", "label": "Q-Resonator", "bonus": 0.1, "adjacency": False, "sc_eligible": True, "image": "q-resonator.png"},
                        {"id": "Xa", "type": "bonus", "label": "Infraknife Accelerator Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Infraknife Accelerator Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Infraknife Accelerator Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                    ],
                },
                                {
                    "label": "Phase Beam",
                    "key": "phase",
                    "modules": [
                        {"id": "PB", "type": "core", "label": "Phase Beam", "bonus": 1.0, "adjacency": False, "sc_eligible": True, "image": "phase-beam.png"},
                        {"id": "FD", "type": "bonus", "label": "Fourier De-Limiter", "bonus": 0.034, "adjacency": False, "sc_eligible": True, "image": "fourier.png"},
                        {"id": "Xa", "type": "bonus", "label": "Phase Beam Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Phase Beam Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Phase Beam Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                    ],
                },
                {
                    "label": "Photon Cannon",
                    "key": "photon",
                    "modules": [
                        {"id": "PC", "type": "core", "label": "Photon Cannon", "bonus": 1.0, "adjacency": False, "sc_eligible": True, "image": "photon.png"},
                        {"id": "NO", "type": "bonus", "label": "Nonlinear Optics", "bonus": 0.1, "adjacency": False, "sc_eligible": True, "image": "nonlinear.png"},
                        {"id": "Xa", "type": "bonus", "label": "Photon Cannon Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Photon Cannon Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Photon Cannon Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                    ],
                },
                {
                    "label": "Positron Ejector",
                    "key": "positron",
                    "modules": [
                        {"id": "PE", "type": "core", "label": "Positron Ejector", "bonus": 1.0, "adjacency": False, "sc_eligible": True, "image": "positron.png"},
                        {"id": "FS", "type": "bonus", "label": "Fragment Supercharger", "bonus": 0.1, "adjacency": False, "sc_eligible": True, "image": "fragment.png"},
                        {"id": "Xa", "type": "bonus", "label": "Positron Ejector Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Positron Ejector Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Positron Ejector Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                    ],
                },
                {
                    "label": "Rocket Launcher",
                    "key": "rocket",
                    "modules": [
                        {"id": "RL", "type": "core", "label": "Rocket Launger", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "rocket.png"},
                        {"id": "LR", "type": "bonus", "label": "Large Rocket Tubes", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "tubes.png"},
                   ],
                },
            ],
             "mobility": [
                 {
                    "label": "Pulse Engine",
                    "key": "pulse",
                    "modules": [
                        {"id": "PE", "type": "core", "label": "Pulse Engine", "bonus": 0.0, "adjacency": False, "sc_eligible": False, "image": "pulse.png"},
                        {"id": "FA", "type": "bonus", "label": "Flight Assist Override", "bonus": 0.11, "adjacency": True, "sc_eligible": False, "image": "flight-assist.png"},
                        {"id": "PC", "type": "reward", "label": "Photonix Core", "bonus": 0.11, "adjacency": True, "sc_eligible": False, "image": "photonix.png"},
                        {"id": "SL", "type": "bonus", "label": "Sub-Light Amplifier", "bonus": 0.00, "adjacency": True, "sc_eligible": False, "image": "sublight.png"},
                        {"id": "ID", "type": "bonus", "label": "Instability Drive", "bonus": 0.00, "adjacency": True, "sc_eligible": False, "image": "sublight.png"},
                        {"id": "Xa", "type": "bonus", "label": "Pulse Engine Upgrade Sigma", "bonus": 0.20, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Pulse Engine Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Pulse Engine Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                    ],
                 },
            ],
             "shields": [
                 {
                    "label": "Starship Shields",
                    "key": "shield",
                    "modules": [
                        {"id": "DS", "type": "core", "label": "Defensive Shields", "bonus": 0.2, "adjacency": False, "sc_eligible": False, "image": "shield.png"},
                        {"id": "AA", "type": "bonus", "label": "Ablative Armor", "bonus": 0.07, "adjacency": False, "sc_eligible": False, "image": "ablative.png"},
                        {"id": "Xa", "type": "bonus", "label": "Shield Upgrade Sigma", "bonus": 0.3, "adjacency": True, "sc_eligible": True, "image": "shield-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Shield Upgrade Tau", "bonus": 0.29, "adjacency": True, "sc_eligible": True, "image": "shield-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Shield Upgrade Theta", "bonus": 0.28, "adjacency": True, "sc_eligible": True, "image": "shield-upgrade.png"},
                    ],
                 },
            ]
        },
    },
    # Add other ships here if needed (e.g., "Fighter", "Hauler")
}

solves = {
    "Exotic": {  # Ship type
        "cyclotron": {
            (0, 0): "CB",
            (1, 0): "Xa",
            (2, 0): "QR",
            (0, 1): "Xb",
            (1, 1): "Xc",
            (2, 1): "None",
        },
        "infra": { 
            (0, 0): "IK",
            (1, 0): "Xa",
            (2, 0): "QR",
            (0, 1): "Xb",
            (1, 1): "Xc",
            (2, 1): None,
        },
        "phase": {
            (0, 0): "PB",
            (1, 0): "Xa",
            (2, 0): "FD",
            (0, 1): "None",
            (1, 1): "Xb",
            (2, 1): "Xc",
        },
        "photon": {
            (0, 0): "PC",
            (1, 0): "Xa",
            (2, 0): "NO",
            (0, 1): "None",
            (1, 1): "Xb",
            (2, 1): "Xc",
        },
        "positron": {
            (0, 0): "PE",
            (1, 0): "Xa",
            (2, 0): "FS",
            (0, 1): "None",
            (1, 1): "Xb",
            (2, 1): "Xc",
        },
        "rocket": {
            (0, 0): "RL",
            (1, 0): "LR",
        },
        "pulse": {
            (0, 0): "ID",
            (1, 0): "Xc",
            (2, 0): "PC",
            (0, 1): "Xb",
            (1, 1): "Xa",
            (2, 1): "SL",
            (0, 2): "PE",
            (1, 2): "FA",
            (2, 2): "None",
        },
        "shield": {
            (0, 0): "DS",
            (1, 0): "Xa",
            (2, 0): "AA",
            (0, 1): "Xc",
            (1, 1): "Xb",
            (2, 1): "None",
        },
    },
}
