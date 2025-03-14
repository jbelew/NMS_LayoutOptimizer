modules = {
    "Exotic": {
        "types": {
            "weapons": [
                {
                    "label": "Cyclotron Ballista",
                    "key": "cyclotron",
                    "modules": [
                        {"id": "CB", "type": "core", "label": "Cyclotron Ballista", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "cyclotron.png"},
                        {"id": "QR", "type": "bonus", "label": "Dyson Pump", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "dyson.png"},
                        {"id": "Xa", "type": "bonus", "label": "Cyclotron Ballista Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Cyclotron Ballista Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Cyclotron Ballista Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "cyclotron-upgrade.png"},
                    ],
                },                
                {
                    "label": "Infraknife Accelerator",
                    "key": "infra",
                    "modules": [
                        {"id": "IK", "type": "core", "label": "Infraknife Accelerator", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "infra.png"},
                        {"id": "QR", "type": "bonus", "label": "Q-Resonator", "bonus": 0.1, "adjacency": False, "sc_eligible": True, "image": "q-resonator.png"},
                        {"id": "Xa", "type": "bonus", "label": "Infraknife Accelerator Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Infraknife Accelerator Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Infraknife Accelerator Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "infra-upgrade.png"},
                    ],
                },
                                {
                    "label": "Phase Beam",
                    "key": "phase",
                    "modules": [
                        {"id": "PB", "type": "core", "label": "Phase Beam", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "phase-beam.png"},
                        {"id": "FD", "type": "bonus", "label": "Fourier De-Limiter", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "fourier.png"},
                        {"id": "Xa", "type": "bonus", "label": "Phase Beam Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Phase Beam Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Phase Beam Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "phase-upgrade.png"},
                    ],
                },
                {
                    "label": "Photon Cannon",
                    "key": "photon",
                    "modules": [
                        {"id": "PC", "type": "core", "label": "Photon Cannon", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "photon.png"},
                        {"id": "NO", "type": "bonus", "label": "Nonlinear Optics", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "nonlinear.png"},
                        {"id": "Xa", "type": "bonus", "label": "Photon Cannon Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Photon Cannon Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Photon Cannon Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "photon-upgrade.png"},
                    ],
                },
                {
                    "label": "Positron Ejector",
                    "key": "positron",
                    "modules": [
                        {"id": "PE", "type": "core", "label": "Positron Ejector", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "positron.png"},
                        {"id": "FS", "type": "bonus", "label": "Fragment Supercharger", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "fragment.png"},
                        {"id": "Xa", "type": "bonus", "label": "Positron Ejector Upgrade Sigma", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Positron Ejector Upgrade Tau", "bonus": 0.19, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Positron Ejector Upgrade Theta", "bonus": 0.18, "adjacency": True, "sc_eligible": True, "image": "positron-upgrade.png"},
                    ],
                },
                {
                    "label": "Rocket Launcher",
                    "key": "rocker",
                    "modules": [
                        {"id": "RL", "type": "core", "label": "Rocket Launger", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "rocket.png"},
                        {"id": "LR", "type": "core", "label": "Large Rocket Tubes", "bonus": 0.1, "adjacency": True, "sc_eligible": True, "image": "tubes.png"},
                   ],
                },
            ],
             "mobility": [
                 {
                    "label": "Pulse Engine",
                    "key": "pulse",
                    "modules": [
                        {"id": "PE", "type": "core", "label": "Pulse Engine", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "pulse.png"},
                        {"id": "FA", "type": "core", "label": "Flight Assist Override", "bonus": 0.07, "adjacency": True, "sc_eligible": False, "image": "flight-assist.png"},
                        {"id": "PC", "type": "core", "label": "Photonix Core", "bonus": 0.07, "adjacency": True, "sc_eligible": False, "image": "photonix.png"},
                        {"id": "SL", "type": "core", "label": "Sub-Light Amplifier", "bonus": 0.07, "adjacency": True, "sc_eligible": False, "image": "sublight.png"},
                        {"id": "Xa", "type": "bonus", "label": "Pulse Engine Upgrade Sigma", "bonus": 0.3, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                        {"id": "Xb", "type": "bonus", "label": "Pulse Engine Upgrade Tau", "bonus": 0.29, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                        {"id": "Xc", "type": "bonus", "label": "Pulse Engine Upgrade Theta", "bonus": 0.28, "adjacency": True, "sc_eligible": True, "image": "pulse-upgrade.png"},
                    ],
                 },
            ],
             "shields": [
                 {
                    "label": "Starship Shields",
                    "key": "shield",
                    "modules": [
                        {"id": "DS", "type": "core", "label": "Defensive Shields", "bonus": 0.2, "adjacency": True, "sc_eligible": True, "image": "shield.png"},
                        {"id": "AA", "type": "core", "label": "Ablative Armor", "bonus": 0.07, "adjacency": True, "sc_eligible": False, "image": "ablative.png"},
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
