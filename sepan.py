from PIL import Image, ImageDraw, ImageFont, ImageFilter
import colorsys
import os
"""
http://blog.csdn.net/taily_duan/article/details/51506776
http://blog.csdn.net/wudaijun/article/details/9964091
"""


color_one = [("null","null","null"),("152,158,35","126,130,57","null"),
				("171,164,66","153,147,63","133,127,49"),("194,165,49","181,153,40","null"),
				("null","null","null"),("204,105,55","194,91,39","null"),("180,75,76","null","null"),
				("183,72,101","176,80,104","153,73,94"),("186,70,122","162,95,124","null"),("null","null","null"),
				("186,61,157","176,74,154","null"),("165,73,173","152,82,158","null"),
				("142,82,175","null","null"),("133,90,165","null","null"),
				("100,50,156","null","null"),("86,51,166","70,58,133","null"),
				("null","null","null"),("null","null","null"),("59,112,135","null","null"),
				("32,116,133","null","null"),("22,120,115","null","null"),
				("null","null","null"),("null","null","null"),("null","null","null")]

def to_hsv( color ):
    """ converts color tuples to floats and then to hsv """
    return colorsys.rgb_to_hsv(*[x/255.0 for x in color]) #rgb_to_hsv wants floats!

def color_dist( c1, c2):
    """ returns the squared euklidian distance between two color vectors in hsv space """
    return sum( (a-b)**2 for a,b in zip(to_hsv(c1),to_hsv(c2)) )

def min_color_diff( color_to_match, colors):
    """ returns the `(distance, color_name)` with the minimal distance to `colors`"""
    return min( # overal best is the best match to any color:
        (color_dist(color_to_match, test), test) # (distance to `test` color, color name)
        for test in colors)

def write_txt(color,txt_name,path):#写入的扩充RGB,写入的色例RGB,写入的目录

    outfile = open(path+"//" + txt_name, 'a', encoding='utf-8')
    color_str = ",".join([str(c) for c in color])
    outfile.writelines(color_str+"\n")

def draw_pic(color,path):
    imageSize = (100, 100)
    image = Image.new("RGB", imageSize, color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("ARIAL.ttf", 15)
    color_str = ",".join([str(c) for c  in color])
    draw.text((10, 50),color_str , font=font)
    # image.show()
    image.save(path+'\\'+color_str+".jpg")

def judugeColorType(color):
    r,g,b =color
    h,s,v = to_hsv(color)
    if (0 <= h <=10/180 or 155/180<h <=1)and (43/255 <=s <=1) and (46/255 <=v <=1):
        return "Red"
    elif (26/180 <= h <=34/180) and (43/255 <=s <=1) and (46/255 <=v <=1):
        return "Yellow"
    elif 0 < h <=1 and 0< s <1 and (0 <=v <=46/255):
        return "Black"
    elif (100/180 <= h <=124/180)and (43/255 <=s <=1) and (46/255 <=v <=1):
        return "Blue"
    else:
        return "Default"





#colorTuple=("152,158,35","126,130,57","null")
def handle_color(colorTuple,store_path):
    print("start to manage a new tuple")
    print(colorTuple)
    for color_str in colorTuple:
        if color_str !="null":
            color = tuple([int(c) for c in color_str.split(",")])
            print(color)
            r_,g_,b_=color
            colorType = judugeColorType(color)
            print(colorType)
            result = []  # 内容格式为((r.g,b),与色例的距离）
            for r in range(r_-50, r_+50, 1):  # 三个for用于穷举所有rgb跟色例rgb算两点间距离
                for g in range(g_-50, g_+50, 1):
                    for b in range(b_-50, b_+50, 1):
                        if colorType == judugeColorType((r,g,b)):
                            dist = color_dist((r, g, b), color)  # 两点间距离
                            result.append(((r, g, b), dist))  # 加入到result数组
            result_sort = sorted(result, key=lambda x: x[1])  # 将结果集根据距离顺序排序
            path = os.path.join(store_path, color_str)
            print(path)
            os.makedirs(path)
            for pic in result_sort[:600]:  # 排名前200的作为扩展色例
                draw_pic(pic[0], path)
                write_txt(pic[0], color_str, path)



if __name__ == '__main__':

    color_nine = [


                  ( "208,186,202", "null"), ("185,152,181", "216,213,218", "null", "null"),
                  ("214,201,202", "null", "null", "null"), ("191,186,197", "null", "null", "null"),
                  ("169,154,185", "185,180,196", "null", "null"), ("129,123,171", "163,157,185", "196,194,203", "null"),
                  ("97,154,183", "129,168,189", "175,102,202", "null"), ("111,160,185", "174,194,206", "null", "null"),
                  ("119,167,188", "155,185,199", "180,196,203", "null"), ("88,162,178", "121,179,194", "160,197,207"),
                  ("70,162,163", "131,186,188", "155,200,201", "null"),
                  ("69,163,151", "141,189,187", "174,202,201", "null"),
                  ("94,170,146", "110,175,153", "162,184,179", "null"),
                  ("98,181,131", "134,194,159", "145,196,168", "null")]
    for colorTuple in color_nine:
        handle_color(colorTuple, "result9")


