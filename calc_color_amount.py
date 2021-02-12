import modules.utils.stroke_loader as stroke_loader
import sys

if __name__ == "__main__":
    args = sys.argv
    strokes = stroke_loader.load(args[1])

    colors = [i.get_color().get_cmykw() for i in strokes]