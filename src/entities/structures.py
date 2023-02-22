all_chords = {
    "major": [0,4,7],
    "minor": [0,3,7],
    "dominant7": [0,4,7,10],
    "m7": [0,3,7,10],
    "maj7": [0,4,7,11],
    "m7b5": [0,3,6,10],
    "dominant7_plus5": [0,4,8,10],
    "dominant7_b5": [0,4,6,10],
    "sus2": [0,2,7],
    "sus4": [0,5,7],
    "m7_plus5": [0,3,8,10],
    "maj7_b5": [0,4,6,11],
    "m_maj7": [0,3,7,11],
    "dimished": [0,3,6,9],
    "augmented": [0,4,8],
    "maj7_plus5":[0,4,8,11]
}

all_scales = {
    "modal_scales": {
        "ionian": {
            "steps": "0,2,4,5,7,9,11",
            "other_modal_names": "dorian,phrygian,lydian,mixolydian,aeolian,locrian"
        },
        "harmonic_minor": {
            "steps": "0,2,3,5,7,8,11",
            "other_modal_names": "locrian_13,ionian_#5,dorian_#11,phrygian_dominant,lydian_#9,harmonic_dimished"
        },
        "melodic_minor":{
            "steps": "0,2,3,5,7,9,11",
            "other_modal_names": "dorian_b9,lydian_augmented,lydian_dominant,mixolydian_b13,locrian_9,superlocrian"
        },
        "harmonic_major":{
            "steps": "0,2,4,5,7,8,11",
            "other_modal_names": "dorian_b5,phrygian_b11,lydian_b3,mixolydian_b9,lydian_augmented_#9,locrian_bb7"
        },
        "double_harmonic_major":{
            "steps": "0,1,4,5,7,8,11",
            "other_modal_names": "lydian_#2_#6,ultraphrygian,double_harmonic_minor,oriental,ionian_augmented_#2,locrian_bb3_bb7"
        },
        "pentatonic_major":{
            "steps": "0,2,4,7,9",
            "other_modal_names": "pentatonic_suspended,pentatonic_blues_minor,pentatonic_blues_major,pentatonic_minor"
        }
    },
    "other_scales":{
        "chromatic": "0,1,2,3,4,5,6,7,8,9,10,11",
        "wholetone": "0,2,4,6,8,10",
        "augmented": "0,3,4,7,8,11",
        "dimished": "0,2,3,5,6,8,9,11",
        "dimished_dominant": "0,1,3,4,6,7,9,10",
        "minor_thirds": "0,3,6,9",
        "major_thirds": "0,4,8",
        "bebop_ionian": "0,2,4,5,7,9,10,11",
        "bebop_dorian" : "0,2,3,4,5,7,9,10",
        "bebop_dorian_altered": "0,2,3,5,7,9,10,11",
        "bebop_harmonic_minor": "0,2,3,5,7,8,10,11",
        "bebop_melodic_minor": "0,2,3,5,7,8,9,11",
        "bebop_dominant": "0,2,4,5,7,9,10,11",
        "blues_minor": "0,3,5,6,7,10",
        "blues_major": "0,2,3,4,7,9",
        "mixo_blues": "0,2,3,4,5,6,8,9,11"
    }
}

all_harmonies = {
    "major": {
        "progression": [
            "maj7",
            "m7",
            "m7",
            "maj7",
            "dominant7",
            "m7",
            "m7b5"
        ],
        "steps": 
            "0,2,4,5,7,9,11"
        
    },
    "minor": {
        "progression": [
            "m7",
            "m7b5",
            "maj7",
            "m7",
            "m7",
            "maj7",
            "dominant7"
        ],
        "steps": 
            "0,2,3,5,7,8,10"
        
    },
    "harmonic_minor": {
        "progression": [
            "m_maj7",
            "m7b5",
            "maj7_plus5",
            "m7",
            "dominant7",
            "maj7",
            "dimished"
        ],
        "steps": 
            "0,2,3,5,7,11"
        
    },
    "melodic_minor": {
        "progression": [
            "m_maj7",
            "m7",
            "maj7_plus5",
            "dominant7",
            "dominant7",
            "m7b5",
            "m7b5"
        ],
        "steps": 
            "0,2,3,5,7,9,11"
        
    },
    "double_harmonic_minor": {
        "progression": [
            "minor",
            ""
        ],
        "steps": ""
    },
    "double_harmonic_major": {
        "progression": [],
        "steps": ""
    },
    "harmonic_major": {
        "progression": [],
        "steps": ""
    }
}