# These value are highly generalized and do not reepresent the actual values in the game. They are ratios derrived from in-game experimentation and used for properly seeding the solving allgorithm.

modules = {
    "Exotic": {
        "types": {
            "weapons": [
                {
                    "label": "Cyclotron Ballista",
                    "key": "cyclotron",
                    "modules": [
                        {"id": "CB", "type": "core", "label": "Cyclotron Ballista", "bonus": 1.0, "adjacency": False, "sc_eligible": True, "image": "cyclotron.png"},
                        {"id": "QR", "type": "bonus", "label": "Dyson Pump", "bonus": 0.04, "adjacency": True, "sc_eligible": True, "image": "dyson.png"},
                        {"id": "Xa", "type": "bonus", "label": "Cyclotron Ballista Upgrade Sigma", "bonus": 0.40, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Cyclotron Ballista Upgrade Tau", "bonus": 0.39, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Cyclotron Ballista Upgrade Theta", "bonus": 0.38, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                    ],
                },                
                {
                    "label": "Infraknife Accelerator",
                    "key": "infra",
                    "modules": [
                        {"id": "IK", "type": "core", "label": "Infraknife Accelerator", "bonus": 1.0, "adjacency": True, "sc_eligible": True, "image": "infra.png"},
                        {"id": "QR", "type": "bonus", "label": "Q-Resonator", "bonus": 0.04, "adjacency": True, "sc_eligible": True, "image": "q-resonator.png"},
                        {"id": "Xa", "type": "bonus", "label": "Infraknife Accelerator Upgrade Sigma", "bonus": 0.40, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Infraknife Accelerator Upgrade Tau", "bonus": 0.39, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Infraknife Accelerator Upgrade Theta", "bonus": 0.38, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                    ],
                },
                                {
                    "label": "Phase Beam",
                    "key": "phase",
                    "modules": [
                        {"id": "PB", "type": "core", "label": "Phase Beam", "bonus": 1.0, "adjacency": True, "sc_eligible": True, "image": "phase-beam.png"},
                        {"id": "FD", "type": "bonus", "label": "Fourier De-Limiter", "bonus": 0.04, "adjacency": True, "sc_eligible": True, "image": "fourier.png"},
                        {"id": "Xa", "type": "bonus", "label": "Phase Beam Upgrade Sigma", "bonus": 0.40, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Phase Beam Upgrade Tau", "bonus": 0.39, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Phase Beam Upgrade Theta", "bonus": 0.38, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                    ],
                },
                {
                    "label": "Photon Cannon",
                    "key": "photon",
                    "modules": [
                        {"id": "PC", "type": "core", "label": "Photon Cannon", "bonus": 1.0, "adjacency": True, "sc_eligible": True, "image": "photon.png"},
                        {"id": "NO", "type": "bonus", "label": "Nonlinear Optics", "bonus": 0.04, "adjacency": True, "sc_eligible": True, "image": "nonlinear.png"},
                        {"id": "Xa", "type": "bonus", "label": "Photon Cannon Upgrade Sigma", "bonus": 0.40, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Photon Cannon Upgrade Tau", "bonus": 0.39, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Photon Cannon Upgrade Theta", "bonus": 0.38, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                    ],
                },
                {
                    "label": "Positron Ejector",
                    "key": "positron",
                    "modules": [
                        {"id": "PE", "type": "core", "label": "Positron Ejector", "bonus": 1.0, "adjacency": True, "sc_eligible": True, "image": "positron.png"},
                        {"id": "FS", "type": "bonus", "label": "Fragment Supercharger", "bonus": 0.04, "adjacency": True, "sc_eligible": True, "image": "fragment.png"},
                        {"id": "Xa", "type": "bonus", "label": "Positron Ejector Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Positron Ejector Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Positron Ejector Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                    ],
                },
                {
                    "label": "Rocket Launcher",
                    "key": "rocket",
                    "modules": [
                        {"id": "RL", "type": "core", "label": "Rocket Launger", "bonus": 1.0, "adjacency": True, "sc_eligible": True, "image": "rocket.png"},
                        {"id": "LR", "type": "bonus", "label": "Large Rocket Tubes", "bonus": 0.056, "adjacency": True, "sc_eligible": True, "image": "tubes.png"},
                   ],
                },
            ],
             "mobility": [
                 {
                    "label": "Hyperdrive",
                    "key": "hyper",
                    "modules": [
                        {"id": "HD", "type": "core", "label": "Hyperdrive", "bonus": 1.0, "adjacency": True, "sc_eligible": False, "image": "hyperdrive.png"},
                        {"id": "AD", "type": "bonus", "label": "Amethyst Drive", "bonus": 0.0, "adjacency": False, "sc_eligible": False, "image": "amethyst.png"},
                        {"id": "CD", "type": "bonus", "label": "Cadmium Drive", "bonus": 0.0, "adjacency": False, "sc_eligible": False, "image": "cadmium.png"},
                        {"id": "ED", "type": "bonus", "label": "Emeril Drive", "bonus": 0.0, "adjacency": False, "sc_eligible": False, "image": "emeril.png"},
                        {"id": "ID", "type": "bonus", "label": "Indium Drive", "bonus": 0.0, "adjacency": False, "sc_eligible": False, "image": "indium.png"},              
                        {"id": "EW", "type": "bonus", "label": "Emergency Warp Unit", "bonus": 0.00, "adjacency": False, "sc_eligible": False, "image": "emergency.png"},
                        {"id": "Xa", "type": "bonus", "label": "Hyperdrive Upgrade Tau", "bonus": .300, "adjacency": True, "sc_eligible": True, "image": "hyper-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Hyperdrive Upgrade Tau", "bonus": .290, "adjacency": True, "sc_eligible": True, "image": "hyper-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Hyperdrive Upgrade Theta", "bonus": .280, "adjacency": True, "sc_eligible": True, "image": "hyper-upgrade.png"},
                    ],
                 },
                 {
                    "label": "Launch Thruster",
                    "key": "launch",
                    "modules": [
                        {"id": "LT", "type": "core", "label": "Launch Thruster", "bonus": 0.0, "adjacency": False, "sc_eligible": False, "image": "launch.png"},
                        {"id": "EF", "type": "bonus", "label": "Efficient Thrusters", "bonus": 0.20, "adjacency": False, "sc_eligible": False, "image": "efficient.png"},
                        {"id": "RC", "type": "bonus", "label": "Launch System Recharger", "bonus": 0.00, "adjacency": False, "sc_eligible": False, "image": "recharger.png"},
                        {"id": "Xa", "type": "bonus", "label": "Launch Thruster Upgrade Sigma", "bonus": 0.30, "adjacency": True, "sc_eligible": True, "image": "launch-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Launch Thruster Upgrade Tau", "bonus": 0.29, "adjacency": True, "sc_eligible": True, "image": "launch-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Launch Thruster Upgrade Theta", "bonus": 0.28, "adjacency": True, "sc_eligible": True, "image": "launch-upgrade.png"},
                    ],
                 },
                 {
                    "label": "Pulse Engine",
                    "key": "pulse",
                    "modules": [
                        {"id": "PE", "type": "core", "label": "Pulse Engine", "bonus": 0.0, "adjacency": False, "sc_eligible": False, "image": "pulse.png"},
                        {"id": "FA", "type": "bonus", "label": "Flight Assist Override", "bonus": 0.08, "adjacency": True, "sc_eligible": False, "image": "flight-assist.png"},
                        {"id": "PC", "type": "reward", "label": "Photonix Core", "bonus": 0.067, "adjacency": True, "sc_eligible": False, "image": "photonix.png"},
                        {"id": "SL", "type": "bonus", "label": "Sub-Light Amplifier", "bonus": 0.00, "adjacency": True, "sc_eligible": False, "image": "sublight.png"},
                        {"id": "ID", "type": "bonus", "label": "Instability Drive", "bonus": 0.00, "adjacency": True, "sc_eligible": False, "image": "instability.png"},
                        {"id": "Xa", "type": "bonus", "label": "Pulse Engine Upgrade Sigma", "bonus": 0.12, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Pulse Engine Upgrade Tau", "bonus": 0.11, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Pulse Engine Upgrade Theta", "bonus": 0.10, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                    ],
                 },
            ],
             "other": [
                 {
                    "label": "Starship Shields",
                    "key": "shield",
                    "modules": [
                        {"id": "DS", "type": "core", "label": "Defensive Shields", "bonus": 1.0, "adjacency": False, "sc_eligible": False, "image": "shield.png"},
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
            "map": {
                (0, 0): "CB",
                (1, 0): "Xa",
                (2, 0): "QR",
                (0, 1): "None",
                (1, 1): "Xb",
                (2, 1): "Xc",
            },
            "score": 5.03
        },
        "infra": {
            "map": {
                (0, 0): "IK",
                (1, 0): "Xa",
                (2, 0): "QR",
                (0, 1): "None",
                (1, 1): "Xb",
                (2, 1): "Xc",
            },
            "score": 5.03
        },
        "phase": {
            "map": {
                (0, 0): "PB",
                (1, 0): "Xa",
                (2, 0): "FD",
                (0, 1): "None",
                (1, 1): "Xb",
                (2, 1): "Xc",
            },
            "score": 5.03
        },
        "photon": {
            "map": {
                (0, 0): "PC",
                (1, 0): "Xa",
                (2, 0): "NO",
                (0, 1): "None",
                (1, 1): "Xb",
                (2, 1): "Xc",
            },
            "score": 5.03
        },
        "positron": {
            "map": {
                (0, 0): "PE",
                (1, 0): "Xa",
                (2, 0): "FS",
                (0, 1): "None",
                (1, 1): "Xb",
                (2, 1): "Xc",
            },
            "score": 5.03
        },
        "rocket": {
            "map": {
                (0, 0): "RL",
                (1, 0): "LR",
            },
            "score": 1.112
        },
        "hyper": {
            "map": {
                (0, 0): "HD",
                (1, 0): "Xb",
                (2, 0): "ED",
                (0, 1): "Xc",
                (1, 1): "Xa",
                (2, 1): "CD",
                (0, 2): "AD",
                (1, 2): "ID",
                (2, 2): "EW",
            },
            "score": 3.78
        },
        "launch": {
            "map": {
                (0, 0): "LT",
                (1, 0): "Xa",
                (2, 0): "EF",
                (0, 1): "Xc",
                (1, 1): "Xb",
                (2, 1): "RC",
            },
            "score": 3.40
        },
        "pulse": {
            "map": {
                (0, 0): "PE",
                (1, 0): "Xb",
                (2, 0): "FA",
                (0, 1): "Xc",
                (1, 1): "Xa",
                (2, 1): "PC",
                (0, 2): "SL",
                (1, 2): "ID",
                (2, 2): "None",
            },
            "score": 1.8810000000000002
        },
        "shield": {
            "map": {
                (0, 0): "DS",
                (1, 0): "Xa",
                (2, 0): "AA",
                (0, 1): "Xc",
                (1, 1): "Xb",
                (2, 1): "None",
            },
            "score": 1.84
        },
    },
}
