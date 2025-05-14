all_chords = {
    "major":{"steps":[0,4,7]
             ,"alias_eng":"Major"
             ,"alias_notation":""},
    "minor":{"steps":[0,3,7]
             ,"alias_eng":"Minor"
             ,"alias_notation":"m"},
    "dominant7":{"steps":[0,4,7,10]
                 ,"alias_eng":"Dominant 7th"
                 ,"alias_notation":"7"},
    "m7":{"steps":[0,3,7,10]
          ,"alias_eng":"Minor 7th"
          ,"alias_notation":"m7"},
    "maj7":{"steps":[0,4,7,11]
            ,"alias_eng":"Maj 7th"
            ,"alias_notation":"maj7"},
    "m7b5":{"steps":[0,3,6,10]
            ,"alias_eng":"Half-dimished 7th"
            ,"alias_notation":"ø"},
    "dominant7_plus5":{"steps":[0,4,8,10]
                       ,"alias_eng":"Dominant 7th #5"
                       ,"alias_notation":"+7"},
    "dominant7_b5":{"steps":[0,4,6,10]
                    ,"alias_eng":"Dominant 7th ♭5"
                    ,"alias_notation":"7♭5"},
    "sus2":{"steps":[0,2,7]
            ,"alias_eng":"Suspended 2"
            ,"alias_notation":"sus2"},
    "sus4":{"steps":[0,5,7]
            ,"alias_eng":"Suspended 4"
            ,"alias_notation":"sus4"},
    "m7_plus5":{"steps":[0,3,8,10]
                ,"alias_eng":"Minor 7th #5"
                ,"alias_notation":"m7#5"},
    "maj7_b5":{"steps":[0,4,6,11]
                ,"alias_eng":"Minor 7th ♭5"
                ,"alias_notation":"m7♭5"},
    "m_maj7":{"steps":[0,3,7,11]
                ,"alias_eng":"Minor Maj 7th"
                ,"alias_notation":"m maj7"},
    "dimished":{"steps":[0,3,6,9]
                ,"alias_eng":"Dimished"
                ,"alias_notation":"dim7"},
    "augmented":{"steps":[0,4,8]
                ,"alias_eng":"Augmented"
                ,"alias_notation":"+"},
    "maj7_plus5":{"steps":[0,4,8,11]
                ,"alias_eng":"Maj 7th #5"
                ,"alias_notation":"maj+7"},
    "maj7_b5":{"steps":[0,4,6,11]
                ,"alias_eng":"Maj 7th ♭5"
                ,"alias_notation":"maj♭7"}
}

all_scales = {
    "modal_scales": {
        "ionian": {
            "steps": [0,2,4,5,7,9,11],
            "other_modal_names": "dorian,phrygian,lydian,mixolydian,aeolian,locrian",
            "aliases_eng": "Ionian,Dorian,Phrygian,Lydian,Mixolydian,Aeolian,Locrian",
            "aliases_pl": "Jońska,Dorycka,Frygijska,Lidyjska,Miksolidyjska,Eolska,Lokrycka"
        },
        "harmonic_minor": {
            "steps": [0,2,3,5,7,8,11],
            "other_modal_names": "locrian_13,ionian_#5,dorian_#11,phrygian_dominant,lydian_#9,harmonic_dimished",
            "aliases_eng": "Harmonic minor,Locrian 13 mode,Ionian #5 mode,Dorian #11 mode,Phrygian dominant,Lydian #9 mode,Harmonic dimished",
            "aliases_pl": "Harmoniczna mol,Lokrycka 13,Jońska #5,Dorycka #11,Frygijska dominantowa,Lidyjska #9,Harmoniczna zmniejszona"

        },
        "melodic_minor":{
            "steps": [0,2,3,5,7,9,11],
            "other_modal_names": "dorian_b9,lydian_augmented,lydian_dominant,mixolydian_b13,locrian_9,superlocrian",
            "aliases_eng": "Melodic minor,Dorian b9 mode,Lydian augmented,Lydian dominant,Mixolydian b13 mode,Locrian 9 mode,Superlocrian",
            "aliases_pl": "Melodyczna mol,Dorycka b9,Lidyjska zwiększona,Lidyjska dominantowa,Mixolidyjska b13,Lokrycka 9,Superlokrycka"
        },
        "harmonic_major":{
            "steps": [0,2,4,5,7,8,11],
            "other_modal_names": "dorian_b5,phrygian_b11,lydian_b3,mixolydian_b9,lydian_augmented_#9,locrian_bb7",
            "aliases_eng": "Harmonic major,Dorian b5 mode,Phrygian b11 mode,Lydian b3 mode,Mixolydian b9,Lydian augmented #9 mode,Locrian bb7 mode",
            "aliases_pl": "Harmoniczna dur,Dorycka b5,Frygijska b11,Lidyjska b3,Miksolidyjska,Lidyjska zwiększona #9,Lokrycka bb7"
        },
        "double_harmonic_major":{
            "steps": [0,1,4,5,7,8,11],
            "other_modal_names": "lydian_#2_#6,ultraphrygian,double_harmonic_minor,oriental,ionian_augmented_#2,locrian_bb3_bb7",
            "aliases_eng": "Double harmonic major,Lydian #2 #6 mode,Ultraphrygian,Double harmonic minor,Oriental,Ionian augmented #2 mode,Locrian bb3 bb7 mode",
            "aliases_pl": "Podwójnie harmoniczna dur,Lidyjska #2 #6,Ultrafrygijska,Podwójnie harmoniczna mol,Orientalna,Jońska zwiększona #2,Lokrycka bb3 bb7"
        },
        "pentatonic_major":{
            "steps": [0,2,4,7,9],
            "other_modal_names": "pentatonic_suspended,pentatonic_blues_minor,pentatonic_blues_major,pentatonic_minor",
            "aliases_eng": "Pentatonic major,Pentatonic suspended,Pentatonic blues minor,Pentatonic blues major,Pentatonic minor",
            "aliases_pl": "Pentatonika dur,Pentatonika sus,Pentatonika blues mol,Pentatonika blues dur,Pentatonika mol"
        }
    },
    "other_scales":{
        "chromatic": {"steps": [0,1,2,3,4,5,6,7,8,9,10,11], "alias_eng": "Chromatic", "alias_pl": "Chromatyczna"},
        "wholetone": {"steps": [0,2,4,6,8,10], "alias_eng": "Wholetone", "alias_pl": "Całotonowa"},
        "augmented": {"steps": [0,3,4,7,8,11], "alias_eng": "Augmented", "alias_pl": "Zwiększona"},
        "dimished": {"steps": [0,2,3,5,6,8,9,11], "alias_eng": "Dimished", "alias_pl": "Zmniejszona"},
        "dimished_dominant": {"steps": [0,1,3,4,6,7,9,10], "alias_eng": "Dimished dominant", "alias_pl": "Zmniejszona dominantowa"},
        "minor_thirds": {"steps": [0,3,6,9], "alias_eng": "Minor thirds", "alias_pl": "Tercje małe"},
        "major_thirds": {"steps": [0,4,8], "alias_eng": "Major thirds", "alias_pl": "Tercje duże"},
        "bebop_ionian": {"steps": [0,2,4,5,7,9,10,11], "alias_eng": "Bebop Ionian", "alias_pl": "Bebop Jońska"},
        "bebop_dorian": {"steps": [0,2,3,4,5,7,9,10], "alias_eng": "Bebop Dorian", "alias_pl": "Bebop Dorycka"},
        "bebop_dorian_altered": {"steps": [0,2,3,5,7,9,10,11], "alias_eng": "Bebop Dorian altered", "alias_pl": "Bebop Dorycka alterowana"},
        "bebop_harmonic_minor": {"steps": [0,2,3,5,7,8,10,11], "alias_eng": "Bebop Harmonic minor", "alias_pl": "Bebop Harmoniczna mol"},
        "bebop_melodic_minor": {"steps": [0,2,3,5,7,8,9,11], "alias_eng": "Bebop Melodic minor", "alias_pl": "Bebop Melodyczna mol"},
        "bebop_dominant": {"steps": [0,2,4,5,7,9,10,11], "alias_eng": "Bebop Dominant", "alias_pl": "Bebop Dominantowa"},
        "blues_minor": {"steps": [0,3,5,6,7,10], "alias_eng": "Blues minor", "alias_pl": "Blues mol"},
        "blues_major": {"steps": [0,2,3,4,7,9], "alias_eng": "Blues major", "alias_pl": "Blues dur"},
        "mixo_blues": {"steps": [0,2,3,4,5,6,8,9,11], "alias_eng": "Mixoblues", "alias_pl": "Mixoblues"},
        "pentatonic_dominant": {"steps": [0,2,4,7,10], "alias_eng": "Pentatonic dominant", "alias_pl": "Pentatonika dominantowa"}
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



all_melodies = [
    {
        "id":'0',
        "name":"Fur Elise",
        "alias_name_pl":"Dla Elizy",
        "notes":[(1,1),(0,1),(1,1),(0,1),(1,1),(-4,1),(-1,1),(-3,1),(-6,2),(-11,1),(-6,1),(-4,2),(-11,1),(-4,1),(-3,3),
                 (1,1),(0,1),(1,1),(0,1),(1,1),(-4,1),(-1,1),(-3,1),(-6,2),(-11,1),(-6,1),(-4,2),(-11,1),(-3,1),(-4,1),(-6,2),
                 (-6,1),(-3,1),(-1,1),(1,2),(-3,1),(2,1),(1,1),(-1,2),(-4,1),(1,1),(-1,1),(-3,2),(-6,1),(-1,1),(-3,1),(-4,3),
                 (1,1),(0,1),(1,1),(0,1),(1,1),(-4,1),(-1,1),(-3,1),(-6,2),(-11,1),(-6,1),(-4,2),(-11,1),(-3,1),(-4,1),(-6,3)
                 ]

    },
    {
        "id":'1',
        "name":"Test",
        "alias_name_pl":'Test PL',
        "notes":[(1,1),(3,1),(5,1)]
    },

]