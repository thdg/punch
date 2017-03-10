from soundscape import SoundScape


def main():

    data = {
        "info_file": "ogg_info.txt",
        "root_folder": "ogg/",
        "delimiter": "\t",
        "path_row": 0,
        "pickup_range": 0.2,
        "delay": 10,
        "dimensions": [
            {
                "row": 1,
                "name": "Env",
                "type": "radio"
            },
            {
                "row": 2,
                "name": "Magic number",
                "type": "float",
                "min": 0,
                "max": 1,
                "default": 0.5,
            },
            {
                "row": 3,
                "name": "Sex",
                "type": "radio",
                "choices": ["male", "female"]
            },
            {
                "row": 4,
                "name": "Age",
                "type": "radio"
            },
            # {
            #     "row": 5,
            #     "name": "Length (char)",
            #     "type": "len"
            # },
            {
                "row": 6,
                "name": "Length (time)",
                "type": "float"
            },
        ]
    }

    ss = SoundScape(data)
    ss.play()

if __name__ == "__main__":
    main()
