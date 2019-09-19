import numpy as np
import typing
import mypy
from typing import Any, List, Dict, Union, Optional
from simplification.cutil import simplify_coords_vw
import time


def sq_seg_dist(p1: int, pi: int, p2: int, i: int, first: int, last: int) -> float:
    """
    Square vertical distance between point and a segment
    """
    dx, dy = last - first, p2 - p1

    if not dx:
        ### dy == 0 because of time series data
        return (pi - p1) ** 2
    else:
        cy = (i - first) * (dy / dx) + p1
        return (pi - cy) ** 2


class compress:
    def __init__(self, points):
        self.points = points

    def modify_dp(self, tolerance: int) -> List[int]:
        start = time.time()

        markers = [0 for _ in range(len(self.points))]

        first, last = 0, len(self.points) - 1

        first_stack, last_stack = [], []

        markers[first], markers[last] = 1, 1

        while last:
            max_sqdist, idx = -1, -1

            for i in range(first + 1, last):
                sq_dist = sq_seg_dist(self.points[i], self.points[first], self.points[last], i, first, last)

                if sq_dist > max_sqdist:
                    idx = i
                    max_sqdist = sq_dist

            if max_sqdist > tolerance:
                markers[idx] = 1

                first_stack.append(first)
                last_stack.append(idx)

                first_stack.append(idx)
                last_stack.append(last)

            first = first_stack.pop() if first_stack else None

            last = last_stack.pop() if last_stack else None

        stop = time.time()
        c_points = [self.points[i] if markers[i] else None for i in range(len(markers))]

        return c_points

    def modify_vw(self, tolerance: int) -> List[int]:
        start = time.time()
        list_param = [[idx, num] for idx, num in enumerate(self.points)]
        c_res = simplify_coords_vw(list_param, tolerance)

        stop = time.time()

        c_idx = 0
        c_points = []

        for idx in range(len(self.points)):
            if idx < c_res[c_idx][0]:
                c_points.append(None)
            elif idx == c_res[c_idx][0]:
                c_points.append(int(c_res[c_idx][1]))
                c_idx += 1

        return c_points

    def circleALG(self, i: int, tolerance: int) -> List[int]:
        length = len(self.points)
        marker = [0 for _ in range(length)]

        marker[0], marker[i], marker[length - 1] = 1, 1, 1

        # Forward direction
        if i < length - 1:
            ratioH, ratioL = self.points[i + 1] + tolerance - self.points[i], self.points[i + 1] - tolerance - \
                             self.points[i]

            k = i + 2
            cur_idx = i

            while k <= length - 1:
                cur_rationH = (self.points[k] + tolerance - self.points[cur_idx]) / (k - cur_idx)
                cur_rationL = (self.points[k] - tolerance - self.points[cur_idx]) / (k - cur_idx)

                if cur_rationH < ratioL or cur_rationL > ratioH:
                    marker[k - 1], marker[k] = 1, 1
                    cur_idx = k
                    if k < length - 1:
                        ratioH, ratioL = self.points[k + 1] + tolerance - self.points[k], self.points[
                            k + 1] - tolerance - self.points[k]
                    k += 2
                else:
                    ratioH, ratioL = min(ratioH, cur_rationH), max(ratioL, cur_rationL)
                    k += 1

        # Backward Direction
        if i > 0:
            ratioH, ratioL = (self.points[i - 1] + tolerance - self.points[i]) / (-1), (
                        self.points[i - 1] - tolerance - self.points[i]) / (-1)

            j = i - 2
            cur_idx = i

            while j > 0:
                cur_rationH = (self.points[j] + tolerance - self.points[cur_idx]) / (j - cur_idx)
                cur_rationL = (self.points[j] - tolerance - self.points[cur_idx]) / (j - cur_idx)

                if cur_rationH > ratioL or cur_rationL < ratioH:
                    marker[j + 1], marker[j] = 1, 1
                    cur_idx = j
                    if j > 0:
                        ratioH, ratioL = (self.points[j] + tolerance - self.points[j - 1]) / (-1), (
                                    self.points[j] - tolerance - self.points[j - 1]) / (-1)
                    j -= 2
                else:
                    ratioH, ratioL = max(ratioH, cur_rationH), min(ratioL, cur_rationL)
                    j -= 1

        return marker


    def modify_opt(self, tolerance: int) -> List[int]:
        start = time.time()
        c_marker = None
        for i in range(len(self.points)):
            marker = self.circleALG(i, tolerance)
            if (not c_marker) or sum(marker) < sum(c_marker):
                c_marker = marker

        c_points = [self.points[i] if c_marker[i] else None for i in range(len(c_marker))]

        return c_points
