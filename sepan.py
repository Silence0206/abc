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
    print(h,s,v)
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
    for color_str in colorTuple:
        print(color_str)
        color = tuple([int(c) for c in color_str.split(",")])
        result = []  # 内容格式为((r.g,b),与色例的距离）
        for r in range(0, 256, 5):  # 三个for用于穷举所有rgb跟色例rgb算两点间距离
            for g in range(0, 256, 5):
                for b in range(0, 256, 5):
                    dist = color_dist((r, g, b), color)  # 两点间距离
                    pec = r / g if g != 0 else 0
                    # print(str(pec))
                    # if pec > 0.9 and pec < 1.1:  # 这个判断可选 如果是绿色系的话规定g的值最大保证色系不变
                    if max(r,g,b) ==b:
                    # if r<70 and g <70 and b<70:
                        result.append(((r, g, b), dist))  # 加入到result数组
                    # draw_pic((r,g,b))
        result_sort = sorted(result, key=lambda x: x[1])  # 将结果集根据距离顺序排序
        # print(result_sort)
        path = os.path.join(store_path, color_str)
        print(path)
        os.makedirs(path)
        for pic in result_sort[:600]:  # 排名前200的作为扩展色例
            draw_pic(pic[0], path)
            write_txt(pic[0], color_str, path)


if __name__ == '__main__':
    color_str = "127,255,255"# h means the part of 360
    print(color_str)
    color = tuple([int(c) for c in color_str.split(",")])
    print(judugeColorType(color))
