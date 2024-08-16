from manimlib import *

import numpy as np


class InteractiveDevelopment(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()

        # 这会打开一个iPython终端，你可以在其中继续写你想要执行的代码
        # 在这个例子中，square/circle/self都会成为终端中的实例
        self.embed()

        # 尝试拷贝粘贴下面这些行到交互终端中
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.play(circle.animate.stretch(4, 0))
        self.play(Rotate(circle, 90 * DEGREES))
        self.play(circle.animate.shift(2 * RIGHT).scale(0.25))

        text = Text("""
            In general, using the interactive shell
            is very helpful when developing new scenes
        """)
        self.play(Write(text))

        # 在交互终端中，你可以使用play, add, remove, clear, wait, save_state
        # 和restore来代替self.play, self.add, self.remove……

        # 这时如果要使用鼠标键盘来与窗口互动，需要输入执行touch()
        # 然后你就可以滚动窗口，或者在按住z时滚动来缩放
        # 按住d时移动鼠标来更改相机视角，按r重置相机位置
        # 按q退出和窗口的交互来继续输入其他代码

        # 特别的，你可以自定一个场景来和鼠标和键盘互动
        always(circle.move_to, self.mouse_point)


class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(r"\beta").get_grid(10, 10, height=4, width=8)
        self.add(grid)

        # 你可以通过.animate语法来动画化物件变换方法
        self.play(grid.animate.shift(LEFT))

        # 这两种方法都会在mobject的初始状态和应用该方法后的状态间进行插值
        # 在本例中，调用grid.shift(LEFT)会将grid向左移动一个单位

        # 这种用法可以用在任何方法上，包括设置颜色
        self.play(grid.animate.set_color(YELLOW))
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        # 方法Mobject.apply_complex_function允许应用任意的复函数
        # 将把Mobject的所有点的坐标看作复数

        self.play(grid.animate.apply_complex_function(np.exp), run_time=10)
        self.wait()
        self.embed()
        # 更一般地说，你可以应用Mobject.apply方法，它接受从R^3到R^3的一个函数
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0],
                    p[1],
                    p[2]
                ]
            ),
            run_time=5,
        )
        self.wait()


class ApplyFuncExample(Scene):
    def construct(self):
        circ = Circle().scale(1)
        circ_ref = circ.copy()
        circ.apply_complex_function(
            lambda x: np.exp(x*1j)
        )
        t = ValueTracker(0)
        circ.add_updater(
            lambda x: x.become(circ_ref.copy().apply_complex_function(
                lambda x: np.exp(x+t.get_value()*1j)
            )).set_color(BLUE)
        )
        self.add(circ_ref)
        self.play(TransformFromCopy(circ_ref, circ))
        self.play(t.animate.set_value(TAU), run_time=4)


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(ShowPartial(circle))  # show the circle on screen


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.play(circle.animate)
        self.embed()


class Show_Position(Scene):
    def construct(self):
        gird1 = Tex(r"\pi").get_grid(10, 10, height=2, width=4)
        gird2 = Tex(r"\pi").get_grid(10, 10, height=2, width=4)
        gird2.animate
        self.wait(2)
        self.play(ShowCreation(gird1))
        self.wait()
        self.play(gird1.animate.apply_function(lambda p: -1 * p))
        self.wait()
        self.play(gird1.animate.apply_function(lambda p: p + 1))
        self.wait()
        gird1.set_height(TAU - MED_SMALL_BUFF)


class TextExample(Scene):
    def construct(self):
        # To run this scene properly, you should have "Consolas" font in your computer
        # for full usage, you can see https://github.com/3b1b/manim/pull/680
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial", font_size=24,
            # t2c is a dict that you can choose color for different text
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, difference).arrange(UP, buff=1)
        self.play(Write(text))
        self.play(Write(difference))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN}
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED}
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text, RIGHT), FadeOut(difference, shift=LEFT))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()


def str_to_slice(slice_str):
    # 去除方括号
    slice_str = slice_str.strip('[]')

    # 分割字符串以提取起始、结束和步长
    parts = slice_str.split(':')

    # 根据部分的数量创建切片
    if len(parts) == 1:
        # 如果只有一个部分，则视为结束位置，开始默认为 None
        return slice(None, int(parts[0]), None)
    elif len(parts) == 2:
        # 如果有两个部分，则视为开始和结束位置
        start = None if parts[0] == '' else int(parts[0])
        stop = None if parts[1] == '' else int(parts[1])
        return slice(start, stop, None)
    elif len(parts) == 3:
        # 如果有三个部分，则视为开始、结束和步长
        start = None if parts[0] == '' else int(parts[0])
        stop = None if parts[1] == '' else int(parts[1])
        step = None if parts[2] == '' else int(parts[2])
        return slice(start, stop, step)
    else:
        raise ValueError("Invalid slice string format")


class Demo(Scene):
    def construct(self):
        text = Text(
            'Google'
        )
        t2c = {
            '[0:1]': '#3174f0', '[1:2]': '#e53125',
            '[2:3]': '#fbb003', '[3:4]': '#3174f0',
            '[4:5]': '#269a43', '[5:6]': '#e53125',
        }
        for i, j in t2c.items():
            sl = str_to_slice(i)
            text[sl.start:sl.stop].set_color(j)
        self.wait(2)
        self.play(Write(text))


script = '''
Hello
你好
こんにちは
안녕하세요
'''


class Demo2(Scene):
    def construct(self):
        text = Text(script, font='Source Han Sans')
        self.play(Write(text))


class TexTransformExample2(Scene):
    def construct(self):
        to_isolate = ["B", "C", "=", "(", ")"]
        lines = VGroup(
            # Passing in muliple arguments to Tex will result
            # in the same expression as if those arguments had
            # been joined together, except that the submobject
            # hierarchy of the resulting mobject ensure that the
            # Tex mobject has a subject corresponding to
            # each of these strings.  For example, the Tex mobject
            # below will have 5 subjects, corresponding to the
            # expressions [A^2, +, B^2, =, C^2]
            Tex("A^2", "+", "B^2", "=", "C^2"),
            # Likewise here
            Tex("A^2", "=", "C^2", "-", "B^2"),
            # Alternatively, you can pass in the keyword argument
            # "isolate" with a list of strings that should be out as
            # their own submobject.  So the line below is equivalent
            # to the commented out line below it.
            Tex("A^2 = (C + B)(C - B)", isolate=["A^2", *to_isolate]),
            # Tex("A^2", "=", "(", "C", "+", "B", ")", "(", "C", "-", "B", ")"),
            Tex("A = \\sqrt{(C + B)(C - B)}", isolate=["A", *to_isolate])
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)
        for line in lines:
            line.set_color_by_tex_to_color_map({
                "A": BLUE,
                "B": TEAL,
                "C": GREEN,
            })

        play_kw = {"run_time": 2}
        self.add(lines[0])
        # The animation TransformMatchingTex will line up parts
        # of the source and target which have matching tex strings.
        # Here, giving it a little path_arc makes each part sort of
        # rotate into their final positions, which feels appropriate
        # for the idea of rearranging an equation
        self.play(
            TransformMatchingTex(
                lines[0].copy(), lines[1],
                path_arc=90 * DEGREES,
            ),
            **play_kw
        )
        self.wait()

        # Now, we could try this again on the next line...
        self.play(
            TransformMatchingTex(lines[1].copy(), lines[2]),
            **play_kw
        )
        self.wait()
        # ...and this looks nice enough, but since there's no tex
        # in lines[2] which matches "C^2" or "B^2", those terms fade
        # out to nothing while the C and B terms fade in from nothing.
        # If, however, we want the C^2 to go to C, and B^2 to go to B,
        # we can specify that with a key map.
        self.play(FadeOut(lines[2]))
        self.play(
            TransformMatchingTex(
                lines[1].copy(), lines[2],
                key_map={
                    "C^2": "C",
                    "B^2": "B",
                }
            ),
            **play_kw
        )
        self.wait()

        # And to finish off, a simple TransformMatchingShapes would work
        # just fine.  But perhaps we want that exponent on A^2 to transform into
        # the square root symbol.  At the moment, lines[2] treats the expression
        # A^2 as a unit, so we might create a new version of the same line which
        # separates out just the A.  This way, when TransformMatchingTex lines up
        # all matching parts, the only mismatch will be between the "^2" from
        # new_line2 and the "\sqrt" from the final line.  By passing in,
        # transform_mismatches=True, it will transform this "^2" part into
        # the "\sqrt" part.
        new_line2 = Tex("A^2 = (C + B)(C - B)", isolate=["A", *to_isolate])
        new_line2.replace(lines[2])
        new_line2.match_style(lines[2])
        self.play(
            TransformMatchingTex(
                new_line2, lines[3], key_map={"^2": "sqrt"}
            ),
            **play_kw
        )
        self.wait(3)
        self.play(FadeOut(lines, RIGHT))

        # Alternatively, if you don't want to think about breaking up
        # the tex strings deliberately, you can TransformMatchingShapes,
        # which will try to line up all pieces of a source mobject with
        # those of a target, regardless of the submobject hierarchy in
        # each one, according to whether those pieces have the same
        # shape (as best it can).
        source = Text("the morse code", height=1)
        target = Text("here come dots", height=1)

        self.play(Write(source))
        self.wait()
        kw = {"run_time": 3, "path_arc": PI / 2}
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()
        self.play(TransformMatchingShapes(target, source, **kw))
        self.wait()


class TexTransformExample(Scene):
    def construct(self):
        to_isolate = ["A", "B", "C", "+", "="]
        lines = VGroup(Tex("A^2 = A^2",isolate=to_isolate), Tex(
            "B^2 + C^2 = A^2",isolate=to_isolate))
        lines.arrange(DOWN, buff=LARGE_BUFF)
        run_kwargs = dict(run_time=2, lag_ratio=0.5)
        self.play(Write(lines[0]),**run_kwargs)
        self.wait()
        self.play(TransformMatchingTex(lines[0].copy(), lines[1],key_map={"^2":"^2"}),**run_kwargs)


class UpdatersExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)

        brace = always_redraw(Brace, square, UP)

        text, number = label = VGroup(
            Text("Width = "),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            )
        )
        label.arrange(RIGHT)

        always(label.next_to, brace, UP)
        f_always(number.set_value, square.get_width)

        self.add(square, brace, label)

        self.play(
            square.animate.scale(2),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait()
        self.play(
            square.animate.set_width(5, stretch=True),
            run_time=3,
        )
        self.wait()
        self.play(
            square.animate.set_width(2),
            run_time=3
        )
        self.wait()

        now = self.time
        w0 = square.get_width()
        square.add_updater(
            lambda m: m.set_width(w0 * math.sin(self.time - now) + w0)
        )
        self.wait(4 * PI)


class ValueTrackerExample(Scene):
    def construct(self):
        number_line = NumberLine()
        pointer = Vector()
        label = Tex("x").add_updater(lambda m: m.next_to(pointer, UP))

        tracker = ValueTracker(0)
        pointer.add_updater(
            lambda m: m.next_to(
                        number_line.n2p(tracker.get_value()),
                        UP
                    )
        )
        self.add(number_line, pointer,label)
        tracker.increment_value(1.5)
        self.wait(1)
        tracker.increment_value(-4)
        self.wait(0.5)
        self.play(tracker.animate.set_value(5))
        self.wait(0.5)
        self.play(tracker.animate.set_value(3))
        self.play(tracker.animate.increment_value(-2))
        self.wait(0.5)

class VectorCoordinateLabel(Scene):
    def construct(self):
        plane = NumberPlane()

        vec_1 = Vector([1, 2])
        vec_2 = Vector([-3, 2])
        label_1 = self.get_coordinate_label(vec_1, color=YELLOW)
        label_2 = self.get_coordinate_label(vec_2, color=BLUE)

        self.add(plane, vec_1, vec_2, label_1, label_2)
    
    def get_coordinate_label(self, vector : Vector, **kwargs):
        coords = vector.get_end()
        s = "\\begin{bmatrix}" + f"{coords[0]} \\\\ {coords[1]}" + "\\end{bmatrix}"
        label = Tex(s, **kwargs)
        label.next_to(vector, vector.get_vector(), SMALL_BUFF)
        if "color" in kwargs:
            label.set_color(kwargs["color"]) 
        return label


class ArrowExample(Scene):
    def construct(self):
        left_group = VGroup()
        # As buff increases, the size of the arrow decreases.
        for buff in np.arange(0, 2.2, 0.45):
            left_group += Arrow(start=LEFT, end=RIGHT)
        # Required to arrange arrows.
        left_group.arrange(DOWN)
        left_group.move_to(4 * LEFT)

        self.add(left_group)