# coding:utf-8

import re


def latex2html(line):
    """识别<latex>标记的数学公式,并使其能够在github中正确显示"""
    pat = re.compile(r"<latex>(.*?)</latex>", re.DOTALL)
    return pat.sub(lambda x: "![](http://latex.codecogs.com/gif.latex?" +
                  re.sub("\s+", "&space;", x.group(1).replace("\\",
                        "\\\\"))+")", line)

def dealwith(mdfile):

    # 更新目录

    ts = False  # 目录开始标记  table start of contents
    es = False  # 目录结束标记  table end of contents
    cd = 0      # 代码部分标记  code
    stext = []  # 存放目录开始前的内容  start text
    etext = []  # 存放目录结束后的内容  end text
    contents = []  # 存放目录内容
    l = stext   # 指定该行存放在那部分内容中

    with open(mdfile, "r", encoding="utf-8") as f:
        for line in f:
            raw_line = line.rstrip("\n")
            line = line.strip()

            if line == "<!--ts-->":  # 目录开始位置
                l.append(raw_line)
                ts = True
            elif line == "<!--te-->":  # 目录结束位置
                es = True
                l = etext
            if ts and not es:  # 如果是目录内容，则跳过不处理
                continue

            if line[:3] == "```":  # 通过cd来检测是否是代码部分
                cd = 1 - cd
            r = re.match(r"(#+)(.+)$", line)
            if r and not cd:  # 如果该行以#开头，且不在代码中，则为标题，处理后添加到
                margin = " " * 3 * (len(r.group(1)) - 1)
                title = r.group(2).strip()
                r = re.match(r"(.*)\[(.*)\]\(.*\)", title)
                if r:
                    title = r.group(1) + r.group(2)
                note = re.findall("[\d\w_-]+", re.sub("\s+", "-", title))
                note = "".join(list(map(str.lower, note)))
                #contents.append(f"{margin}* [{title}](#{note})")
                contents.append("{}* [{}](#{})".format(margin, title, note))

            l.append(raw_line)

    # 更新数学公式（github）
    stext = latex2html("\n".join(stext))
    content = "\n".join(contents)
    etext = latex2html("\n".join(etext))

    with open(mdfile, "w", encoding="utf-8") as f:
        if etext:
            f.write(stext + "\n" + content + "\n" + etext)
        else:
            f.write(content + "\n" + stext)


if __name__ == "__main__":

    import argparse

    desc = """
修改markdown文件，是能够在github中正常显示
  1. 添加目录结构
  2. 将<latex>标记的公式，在github中正确显示
"""
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("md_files", nargs="*")
    args = parser.parse_args()

    for md_file in args.md_files:
        dealwith(md_file)

