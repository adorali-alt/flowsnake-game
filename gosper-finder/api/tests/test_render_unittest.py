from wolframclient.language import wl
from wolframclient.evaluation import WolframLanguageSession

import unittest
from unittest import IsolatedAsyncioTestCase
import sys
import os

sys.path.append(os.getcwd()) 

import coords
import game_state_manager
import rendering_utils
import coords_and_segments_graph
import tetrahedral_disphenoid
import triangular_plane
import game_state_manager
from line import *

from solid import *
from solid.utils import *
from euclid3 import Point3
from math import cos, radians, sin, pi, tau
from wolframclient.language import wl
from wolframclient.evaluation import SecuredAuthenticationKey, WolframCloudAsyncSession
from wolframclient.deserializers import binary_deserialize
import asyncio


class TestRender(IsolatedAsyncioTestCase):

    # def test_openscad_drawing(self):
    #     d = union()(
    #         cube(10),  
    #         right(15)(sphere(15))
    #     )
    #     scad_render_to_file(d, os.path.abspath('out/test/basic.scad'))

    # def test_polyline_3d(self):
    #     points = [[1, 2, 3], [4, -5, -6], [-1, -3, -5], [0, 0, 0]]
    #     l = polyline3D.polyline3D(points)
    #     scad_render_to_file(l, os.path.abspath('out/test/polyline3d.scad'))
    # async def test_render_2d_l_system(self):
    #     # start wolfram client 

    #     # SecuredAuthenticationKey[Association["Name" -> "Untitled Application 3", 
    #     # "ApplicationID" -> 55848, "ManagementFunctions" -> True, "LocallyEnabled" -> True, 
    #     # "RequestTokenURL" -> "https://account.wolfram.com/auth/request-token", 
    #     # "AccessTokenURL" -> "https://account.wolfram.com/auth/access-token", "OAuthVersion" -> "1.0a", "OAuthType" -> "TwoLegged", 
    #     # "ConsumerKey" -> "BJrDHA3GH2FfUfDRALzbII3DxprIjilerX663I7cgTY=", 
    #     # "ConsumerSecret" -> "5/fbh70vjt4KyxJnVFKBnMn7CMiyw3gYtXZwg68rT2Q=", "SignatureMethod" -> {"HMAC", "SHA1"}, "TransmissionMethod" -> "Headers"]],
    #     key = SecuredAuthenticationKey(
    #         'BJrDHA3GH2FfUfDRALzbII3DxprIjilerX663I7cgTY=',
    #         '5/fbh70vjt4KyxJnVFKBnMn7CMiyw3gYtXZwg68rT2Q=')

    #     async with WolframCloudAsyncSession(credentials=key) as session:
    #         await session.start()
    #         assert session.authorized()

    #         s = await session.evaluate(wl.Graphics(wl.Line(wl.AnglePath(wl.StringCases(wl.First(
    #                 wl.SubstitutionSystem(wl.wlexpr('{"F" -> "F-F+F+FFF-F-F+F"}'), "F", 3), 
    #                 [wl.wlexpr('"F" -> {1, 0}'), wl.wlexpr('"-" -> {0, Pi/2}'), wl.wlexpr('"+" -> {0, -Pi/2}')])
    #             )))))

    #         # works
    #         # r = await session.evaluate(wl.StringReverse("cba"))

    #         ss = {"A": "AB+BA+B", "B": "B+AAB"}
    #         stri = await session.evaluate(wl.SubstitutionSystem(ss, "A", 1))

    #         # cases = await session.evaluate(wl.StringCases[stri, {"A" -> {1, 0}, "B" -> {0, Pi/2}, "+" -> {0, -Pi/2}}])
    #         print(stri)

    #         # wxf_out = await session.evaluate(wl.export(wl.wlexpr('''                
    #         #     EmbedCode[ Graphics[ Line@AnglePath@StringCases[First@SubstitutionSystem[{"F" -> "F-F+F+FFF-F-F+F"}, "F", {3}], {"F" -> {1, 0}, "-" -> {0, Pi/2}, "+" -> {0, -Pi/2}}]]]
    #         # '''), target_format="wxf"))

    #         # s = binary_deserialize(wxf_out)


    #         # print(session.evaluate(wl.export(wl.wlexpr('''
    #         #     Graphics3D[{Red, Polygon[{{0, 0, 0}, {0, 1, 0}, {0, 1, 1}}], Green, Polygon[0.0000001 + {{0, 0, 0}, {0, 1, 0}, {0, 1, 1}}]}]
    #         # '''), target_format='wxf')))
    #         # self.assertEqual('cba', r)
    #         # print(session.evaluate(wl.export(wl.wlexpr('''
    #         #     Graphics3D[Tube[AnglePath3D[ConstantArray[{100. °, 100. °, 100. °}, 20]]], Boxed -> False]
    #         # '''), target_format='wxf')))
    #         # session.evaluate(wl.wlexpr('''
    #         #     Graphics3D[Tube[AnglePath3D[ConstantArray[{100. °, 100. °, 100. °}, 20]]], Boxed -> False]
    #         # '''))

    #         await session.stop()

    def test_change_of_basis_matrices(self):
        print("WAL copiable statement:")
        print("Graphics3D[Prism[{{1, 0, 1}, {0, 0, 0}, {2, 0, 0}, {1, 2, 1}, {0, 2, 0}, {2, 2, 0}}]]\n")
        print(self.format_fixer(rendering_utils.render_segments_3D(self.spawn_triangular_plane_in(coords.Coords(0,0,0)).get_segments_array())))

    # i think the problem is that the skipped tetras dont always line up correctly. tetras where there should be holes. 
    #  double and triple check all that work carefully. it renders so yay, good work :]
    #  https://www.wolframcloud.com/env/194aad71-9dfb-4b10-9b5d-19f32498735f
    def test_generator_render(self):
        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(2, True)

        print("WAL copiable statement:")
        print("Graphics3D[Prism[{{1, 0, 1}, {0, 0, 0}, {2, 0, 0}, {1, 2, 1}, {0, 2, 0}, {2, 2, 0}}]]\n")
        print(self.format_fixer(rendering_utils.render_segments_3D(generator_flag_graph.get_all_segments())))


    def format_fixer(self, prisms_array):
        result = ""
        for prism in prisms_array:
            result += "Prism[{"
            for c in prism:
                result += "{"
                result += str(c[0])
                result += ", "
                result += str(c[1])
                result += ", "
                result += str(c[2])
                result += "},"
            result += "}],"
        result += "]"
        return result


    # SETUP UTILS

    # c :: Coords, top corner of the pyramid to have its triangles spawned.
    # Returns GeneratorFlag 
    # Not like in 2D, will spawn BOTH flags associated with this pyramid's octahedron not just one. 
    # left inner then right outer
    # see CoordsAndSegmentsGraph for definition
    def spawn_triangular_plane_in(self, c):
        # t, s, b
        return tetrahedral_disphenoid.Tetra(
                    [self.spawn_flag_2D(c, c.posIncrUpIn(), c.posIncrLeftIn()), 
                    self.spawn_flag_2D(c.posIncrUpIn(), c, c.posIncrDownIn()), 
                    self.spawn_flag_2D(c.posIncrLeftIn(), c, c.posIncrDownIn()),
                    self.spawn_flag_2D(c.posIncrUpIn(), c.posIncrLeftIn(), c.posIncrDownIn())])

    # c :: Coords, left corner of the flag to have its segments spawned (in 2D looks like '<|')
    # Returns GeneratorFlag 
    def spawn_flag_2D(self, c1, c2, c3):
        return triangular_plane.Tri(c2,
            [Line(0, Direction.SW, c1, c2),
            Line(0, Direction.SE, c2, c3),
            Line(0, Direction.N, c3, c1)],
            0)

        


    # WAL QUERIES

    # def test_render_all_flags(self):
    #     generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(2)

        # with WolframLanguageSession('/Applications/Wolfram Engine.app/Contents/MacOS/WolframKernel') as session:
        #     print("session started")
        #     print(session.evaluate(wl.export(wl.wlexpr('''
        #         Graphics3D[{Red, Polygon[{{0, 0, 0}, {0, 1, 0}, {0, 1, 1}}], Green, Polygon[0.0000001 + {{0, 0, 0}, {0, 1, 0}, {0, 1, 1}}]}]
        #     '''), target_format='wxf')))
        #     self.assertEqual('cba', session.evaluate(wl.StringReverse('abc')))
        #     # print(session.evaluate(wl.export(wl.wlexpr('''
        #     #     Graphics3D[Tube[AnglePath3D[ConstantArray[{100. °, 100. °, 100. °}, 20]]], Boxed -> False]
        #     # '''), target_format='wxf')))
        #     # session.evaluate(wl.wlexpr('''
        #     #     Graphics3D[Tube[AnglePath3D[ConstantArray[{100. °, 100. °, 100. °}, 20]]], Boxed -> False]
        #     # '''))

    #     print('done')

        # v openscad render code
        # flags_union = union()
        # for flag in generator_flag_graph.get_all_flags():
        #     flags_union.add(polyline3D.polyline3D(flag.get_all_coords_renderable()))
        # scad_render_to_file(flags_union, os.path.abspath('out/test/test_all_flags_2D.scad'))

        # generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(2, True)
        # flags_union = union()
        # for flag in generator_flag_graph.get_all_flags():
        #     flags_union.add(polyline3D.polyline3D(flag.get_all_coords_renderable()))
        # scad_render_to_file(flags_union, os.path.abspath('out/test/test_all_flags_3D.scad'))

    # def test_render_path(self):
    #     manager = game_state_manager.GameStateManager(2)
    #     manager.auto_solve()

    #     path_union = union()
    #     for segment in manager.get_selected_path_stack():
    #         path_union.add(polyline3D.polyline3D(segment.get_all_coords_renderable()))

    #     scad_render_to_file(path_union, os.path.abspath('out/test/test_path_2D.scad'))

        # manager = game_state_manager.GameStateManager(2, True)
        # manager.auto_solve()

        # path_union = union()
        # # s = list(manager.get_selected_path_stack())#[len(manager.get_selected_path_stack()) - 4:len(manager.get_selected_path_stack()) - 3]
        # for segment in manager.get_selected_path_stack():
        #     path_union.add(polyline3D.polyline3D(segment.get_all_coords_renderable()))

        # scad_render_to_file(path_union, os.path.abspath('out/test/test_path_3D.scad'))


    # def test_wolfram_angle3D(self):

    #     with WolframLanguageSession('/Applications/Wolfram Engine.app/Contents/MacOS/WolframKernel') as session:
    #         print("session started")
    #         print(session.evaluate(wl.export(wl.wlexpr('''
    #             Graphics3D[{Red, Polygon[{{0, 0, 0}, {0, 1, 0}, {0, 1, 1}}], Green, Polygon[0.0000001 + {{0, 0, 0}, {0, 1, 0}, {0, 1, 1}}]}]
    #         '''), target_format='wxf')))
    #         self.assertEqual('cba', session.evaluate(wl.StringReverse('abc')))
    #         # print(session.evaluate(wl.export(wl.wlexpr('''
    #         #     Graphics3D[Tube[AnglePath3D[ConstantArray[{100. °, 100. °, 100. °}, 20]]], Boxed -> False]
    #         # '''), target_format='wxf')))
    #         # session.evaluate(wl.wlexpr('''
    #         #     Graphics3D[Tube[AnglePath3D[ConstantArray[{100. °, 100. °, 100. °}, 20]]], Boxed -> False]
    #         # '''))

    #     print('done')


if __name__ == '__main__':
    unittest.main()

# RUN WITH python test_render_unittest.py
# see https://docs.python.org/3/library/unittest.html
