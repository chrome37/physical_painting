class DefinedPositions:
    def __init__(self):
        self.i00 = PulseCoord(-67000, -20000, 124000, 0, 60000, -15000, 0)
        self.i01 = PulseCoord(0, -8000, 145000, 0, -38000, 52212, 0)
        self.i02 = PulseCoord(40000, -20000, 124000, 0, 60000, -15000, 0)
        self.i03 = PulseCoord(39000, -8000, 145000, 0, -38000, 52212, 0)

        self.b00 = PulseCoord(-46678, -21373, 121754, 166, 60711, -26186, 0)
        self.b01 = PulseCoord(-46678, -45910, 124470, 295, 30466, -26268, 0)
        self.b10 = PulseCoord(-57838, -36720, 94764, 52, 70458, -19827, 0)
        self.b11 = PulseCoord(-57838, -55883, 97442, 70, 46283, -19840, 0)
        self.b20 = PulseCoord(-70338, -11030, 137576, 2447, 56558, -18743, 9737)
        self.b21 = PulseCoord(-66244, -40653, 140632, 10294, 20422, -22260, 4855)
        self.b30 = PulseCoord(-76242, -28977, 109154, 4164, 64925, -14209, 7408)
        self.b31 = PulseCoord(-74414, -50530, 111768, 6478, 38117, -15084, 4724)
        self.b40 = PulseCoord(-56381, -5461, 145642, -4228, 55569, -1978, -34032)
        self.b41 = PulseCoord(-71497, -39534, 148973, -42870, 17701, 15346, -17000)
        self.b50 = PulseCoord(-68384, -27092, 115299, -15028, 63978, 3440, -28116)
        self.b51 = PulseCoord(-76236, -49258, 117984, -24555, 36359, 7166, -16921)

        self.w00 = PulseCoord(-91117, -31097, 109397, -18320, 66615, 17329, -30863)
        self.w01 = PulseCoord(-95153, -40677, 112972, -22573, 52242, 18919, -24843)
        self.w02 = PulseCoord(-77470, -10402, 141791, -10961, 56720, 19377, -49704)
        self.w03 = PulseCoord(-93670, -30019, 146349, -32654, 33209, 28882, -31519)
        self.w03_touch = PulseCoord(-97805, -30794, 144386, -31840, 34102, 30299, -30738)
        self.w04 = PulseCoord(-88344, -26969, 117357, -18729, 64008, 18813, -35406)
        self.w05 = PulseCoord(-91539, -31542, 119713, -20997, 56388, 19685, -31003)
        self.w05_large = PulseCoord(-91122, -30868, 119452, -20657, 57419, 19557, -31578)
        self.w06_large = PulseCoord(-88322, -26390, 128489, -21507, 54310, 21680, -36858)
        self.w06 = PulseCoord(-89098, -27236, 128500, -21910, 53285, 21771, -35799)
        self.w07 = PulseCoord(-83613, -22356, 126190, -19140, 61441, 20730, -42896)
        self.w08 = PulseCoord(-90736, -30267, 119214, -20365, 58346, 19430, -32127)

        self.p00 = PulseCoord(44687, -58797, 50941, 24, 89413, -17655, 0)
        self.p01 = PulseCoord(46577, -63244, 60374, 41, 74996, -18731, 0)
        self.p01_right_up = PulseCoord(45277, -60666, 66078, 29, 72180, -17993, 0)
        self.p01_left_up = PulseCoord(47665, -65614, 55129, 51, 77577, -19349, 0)
        self.p01_right = PulseCoord(45276, -61439, 66174, 29, 71219, -17993, 0)
        self.p01_left = PulseCoord(47665, -66362, 55238, 51, 76628, -19349, 0)
        self.p02 = PulseCoord(46577, -61391, 59839, 41, 77687, -18731, 0)
        self.p03 = PulseCoord(42730, -72166, 36266, 10,	89168, -16546, 0)
        self.p04 = PulseCoord(42730, -69765, 33201, 10,	94930, -16546, 0)
        self.p05 = PulseCoord(46581, -58237, 57875, 33,	83193, -18738, 0)

class PulseCoord:
    def __init__(self, s, l, u, r, b, t, e):
        self.mode = "p"
        self.s = s
        self.l = l
        self.u = u
        self.r = r
        self.b = b
        self.t = t
        self.e = e

    def get_list(self):
        return [self.s, self.l, self.u, self.r, self.b, self.t, self.e]

class RobotCoord:
    def __init__(self, x, y, z, r_x, r_y, r_z, thickness):
        self.mode = "r"
        self.x = x
        self.y = y
        self.z = z
        self.r_x = r_x
        self.r_y = r_y
        self.r_z = r_z
        self.thickness = thickness

    def get_list(self):
        return [self.x, self.y, self.z, self.r_x, self.r_y, self.r_z, self.thickness]
