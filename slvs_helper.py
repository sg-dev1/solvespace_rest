import slvs
import math
import numbers

# Taken from slvs.h
SLVS_RESULT_OKAY=0
SLVS_RESULT_INCONSISTENT=1
SLVS_RESULT_DIDNT_CONVERGE=2
SLVS_RESULT_TOO_MANY_UNKNOWNS=3

ROUND_DIGITS = 6

class Slvs_Helper():
    def __init__(self):
        self.sys = slvs.System()
        self.workPlaneGroup = 1
        self.solveGroup = 2
        # entity ids
        self.xyPlaneId = 1
        self.xzPlaneId = 2
        self.yzPlaneId = 3
        self.originId = 4
        self.xyNormalId = 5
        self.xzNormalId = 6
        self.yzNormalId = 7

        self._genOrigin()
        self._genXyPlane()
        self._genXzPlane()
        self._genYzPlane()

        self._paramId = 100
        self._circleDistanceId = 100
        self._entityIdBase = 1000
        self._constraintIdBase = 1

        self._pointDataLst = []
        self._circleDataLst = []

    def _genOrigin(self):
        # origin (x y z) = (0 0 0) of coordinate system
        self.sys.addParam(slvs.makeParam(1, self.workPlaneGroup, 0))
        self.sys.addParam(slvs.makeParam(2, self.workPlaneGroup, 0))
        self.sys.addParam(slvs.makeParam(3, self.workPlaneGroup, 0))
        self.sys.addEntity(slvs.makePoint3d(self.originId, self.workPlaneGroup, 1, 2, 3))
    # working planes
    def _genXyPlane(self):
        # xy plane with basis vectors (1 0 0) and (0 1 0)
        q = slvs.makeQuaternion(1, 0, 0, 0, 1, 0)

        self.sys.addParam(slvs.makeParam(4, self.workPlaneGroup, q[0]))
        self.sys.addParam(slvs.makeParam(5, self.workPlaneGroup, q[1]))
        self.sys.addParam(slvs.makeParam(6, self.workPlaneGroup, q[2]))
        self.sys.addParam(slvs.makeParam(7, self.workPlaneGroup, q[3]))
        self.sys.addEntity(slvs.makeNormal3d(self.xyNormalId , self.workPlaneGroup, 4, 5, 6, 7))
        self.sys.addEntity(slvs.makeWorkplane(self.xyPlaneId, self.workPlaneGroup, self.originId, self.xyNormalId ))
    def _genXzPlane(self):
        # xz plane with basis vectors (1 0 0) and (0 0 1)
        q = slvs.makeQuaternion(1, 0, 0, 0, 0, 1)

        self.sys.addParam(slvs.makeParam(8, self.workPlaneGroup, q[0]))
        self.sys.addParam(slvs.makeParam(9, self.workPlaneGroup, q[1]))
        self.sys.addParam(slvs.makeParam(10, self.workPlaneGroup, q[2]))
        self.sys.addParam(slvs.makeParam(11, self.workPlaneGroup, q[3]))
        self.sys.addEntity(slvs.makeNormal3d(self.xzNormalId , self.workPlaneGroup, 8, 9, 10, 11))
        self.sys.addEntity(slvs.makeWorkplane(self.xzPlaneId, self.workPlaneGroup, self.originId, self.xzNormalId ))
    def _genYzPlane(self):
        # yz plane with basis vectors (0 1 0) and (0 0 1)
        q = slvs.makeQuaternion(0, 1, 0, 0, 0, 1)

        self.sys.addParam(slvs.makeParam(12, self.workPlaneGroup, q[0]))
        self.sys.addParam(slvs.makeParam(13, self.workPlaneGroup, q[1]))
        self.sys.addParam(slvs.makeParam(14, self.workPlaneGroup, q[2]))
        self.sys.addParam(slvs.makeParam(15, self.workPlaneGroup, q[3]))
        self.sys.addEntity(slvs.makeNormal3d(self.yzNormalId , self.workPlaneGroup, 12, 13, 14, 15))
        self.sys.addEntity(slvs.makeWorkplane(self.yzPlaneId, self.workPlaneGroup, self.originId, self.yzNormalId ))

    def _planeStrToPlaneId(self, plane):
        planeId = -1
        if plane == "xy":
            planeId = self.xyPlaneId
        elif plane == "xz":
            planeId = self.xzPlaneId
        elif plane == "yz":
            planeId = self.yzPlaneId
        else:
            assert False, "Invalid plane %s given." % plane
        return planeId
        
    def _planeStrToNormalId(self, plane):
        normalId = -1
        if plane == "xy":
            normalId = self.xyNormalId
        elif plane == "xz":
            normalId = self.xzNormalId
        elif plane == "yz":
            normalId = self.yzNormalId
        else:
            assert False, "Invalid plane %s given." % plane
        return normalId

    def addPoint(self, plane, idHint, data):
        planeId = self._planeStrToPlaneId(plane)

        # Select the proper points (according to plane)
        if planeId == self.xyPlaneId:
            u = data[0] # x
            v = data[1] # y
        elif planeId == self.xzPlaneId:
            u = data[0] # x
            v = data[2] # z
        elif planeId == self.yzPlaneId:
            u = data[2] # y
            v = data[1] # z
        else:
            assert False, "Unknown plane id %d" % planeId
            
        u = round(u, ROUND_DIGITS)
        v = round(v, ROUND_DIGITS)

        p1Id = self._paramId
        self.sys.addParam(slvs.makeParam(p1Id, self.solveGroup, u))
        self._paramId = self._paramId + 1
        p2Id = self._paramId
        self.sys.addParam(slvs.makeParam(p2Id, self.solveGroup, v))
        self._paramId = self._paramId + 1

        print("Make point with id %d and coords (%.3f, %.3f). Input coords: (%.3f, %.3f, %.3f)" % (idHint, u, v, data[0], data[1], data[2]))

        self.sys.addEntity(slvs.makePoint2d(idHint + self._entityIdBase, self.solveGroup, planeId, p1Id, p2Id))

        self._pointDataLst.append({"id": idHint + self._entityIdBase, "params": (p1Id, p2Id), "vals": (u, v)})

    def addLine(self, plane, idHint, data):
        planeId = self._planeStrToPlaneId(plane)

        print("add line with id %d and data %s" % (idHint, str(data)))

        self.sys.addEntity(
            slvs.makeLineSegment(idHint + self._entityIdBase, self.solveGroup, planeId, data[0] + self._entityIdBase, data[1] + self._entityIdBase)
            )
            
    def addCircle(self, plane, idHint, data):
        if (self._circleDistanceId >= self._entityIdBase):
            # Note: With _circleDistanceId starting at 100 and _entityIdBase being 1000 we can draw up to 
            #       900 circles in a sketch
            print("Error adding circle with id %d and data %s. Too much circles drawn in sketch." % (idHint, str(data)))
            return
    
        planeId = self._planeStrToPlaneId(plane)
        normalId = self._planeStrToNormalId(plane)

        print("add circle with id %d and data %s" % (idHint, str(data)))
        
        radiusParamId = self._paramId
        radiusValue = round(data[1], ROUND_DIGITS)
        self.sys.addParam(slvs.makeParam(radiusParamId, self.solveGroup, radiusValue))
        self._paramId = self._paramId + 1
        
        # The radius of a circle must also be an entity of type distance
        circleDistanceId = self._circleDistanceId
        self.sys.addEntity(
            slvs.makeDistance(circleDistanceId, self.solveGroup, planeId, radiusParamId)
            )
        self._circleDistanceId = self._circleDistanceId + 1
        
        self.sys.addEntity(
            slvs.makeCircle(idHint + self._entityIdBase, self.solveGroup, planeId, data[0] + self._entityIdBase, normalId,  circleDistanceId)
            )
            
        self._circleDataLst.append({"id": idHint + self._entityIdBase, "params": (radiusParamId, data[0] + self._entityIdBase), "vals": (radiusValue, )})
    
    def _getEntityId(self, entityIdStr):
        if isinstance(entityIdStr, numbers.Number):
            return entityIdStr + self._entityIdBase
        else:
            if "zero" == entityIdStr:
                return self.originId
            else:
                raise ValueError("Unknown entity id %s received." % str(entityIdStr))
                
    def _getCoordsForPoint(self, pointId):
        point_x_param = self.sys.getEntityParam(pointId, 0)
        point_y_param = self.sys.getEntityParam(pointId, 1)
        point_x = self.sys.getParam(point_x_param).val
        point_y = self.sys.getParam(point_y_param).val
        #print(pointId, point_x_param, point_y_param, point_x, point_y)
        return (point_x, point_y)
    
    def addConstraint(self, plane, idHint, constraintType, data):
        planeId = self._planeStrToPlaneId(plane)

        print("add constraint with id %d and type %d and data %s" % (idHint, constraintType, str(data)))

        valA = round(data[0], ROUND_DIGITS)
        ptA = 0
        if data[1] != 0:
            ptA = self._getEntityId(data[1])
        ptB = 0
        if data[2] != 0:
            ptB = self._getEntityId(data[2])
        entityA = 0
        if data[3] != 0:
            entityA = self._getEntityId(data[3])
        entityB = 0
        if data[4] != 0:
            entityB = self._getEntityId(data[4])

        print("\t%.3f, %d, %d, %d, %d" % (valA, ptA, ptB, entityA, entityB))
        
        c = slvs.makeConstraint(idHint + self._constraintIdBase, self.solveGroup, constraintType, planeId, valA, ptA, ptB, entityA, entityB)
        if constraintType == slvs.SLVS_C_ANGLE:
            #line1 = self.sys.getEntity(entityA)
            #line2 = self.sys.getEntity(entityB)
            #print(line1)
            #print(line2)
            # Endpoints of line1
            point1_1 = self.sys.getEntityPoint(entityA, 0)
            point1_1_x, point1_1_y = self._getCoordsForPoint(point1_1)
            point2_1 = self.sys.getEntityPoint(entityA, 1)
            point2_1_x, point2_1_y = self._getCoordsForPoint(point2_1)
            # vector of line 1
            v1 = (point2_1_x - point1_1_x, point2_1_y - point1_1_y)
            # Endpoints of line 2
            point1_2 = self.sys.getEntityPoint(entityB, 0)
            point1_2_x, point1_2_y = self._getCoordsForPoint(point1_2)
            point2_2 = self.sys.getEntityPoint(entityB, 1)
            point2_2_x, point2_2_y = self._getCoordsForPoint(point2_2)
            # vector of line 2
            v2 = (point2_2_x - point1_2_x, point2_2_y - point1_2_y)
            #print(v1)
            #print(v2)
            # different cases for points that were added first and points that were added later
            if point2_1 <= point1_2 and point2_1 <= point2_2:
                #print("case1")
                # distance squared from endpoint of first line to start point of second line
                x1 = (point2_1_x - point1_2_x)**2 + (point2_1_y - point1_2_y)**2
                # distance squared from endpoint of first line to endpoint of second line
                x2 = (point2_1_x - point2_2_x)**2 + (point2_1_y - point2_2_y)**2
                #print(x1)
                #print(x2)
                if x1 < x2:
                    #print("--- need a swap ---")
                    c.other = True
            else:
                #print("case2")
                # distance squared start of first line to end of second line
                x1 = (point1_1_x - point2_2_x)**2 + (point1_1_y - point2_2_y)**2
                # distance squared from endpoint of first line to endpoint of second line
                x2 = (point2_1_x - point2_2_x)**2 + (point2_1_y - point2_2_y)**2
                #print(x1)
                #print(x2)
                if x1 < x2:
                    #print("--- need a swap ---")
                    c.other = True
            

        self.sys.addConstraint(c)

    def solve(self):
        result = self.sys.solve(self.solveGroup, True)

        if result == SLVS_RESULT_OKAY:
            changedEntities = []
            for p in self._pointDataLst:
                u = round(self.sys.getParam(p["params"][0]).val, ROUND_DIGITS)
                v = round(self.sys.getParam(p["params"][1]).val, ROUND_DIGITS)
                if not math.isclose(u, p["vals"][0], rel_tol=1e-3) or not math.isclose(v, p["vals"][1], rel_tol=1e-3):
                    # substract the self._entityIdBase to get the orginal id sent by the frontend
                    changedEntities.append({"id": p["id"] - self._entityIdBase, "t": "point", "v": [u, v]})
            for c in self._circleDataLst:
                radius = round(self.sys.getParam(c["params"][0]).val, ROUND_DIGITS)
                if not math.isclose(radius, c["vals"][0], rel_tol=1e-3):
                    # substract the self._entityIdBase to get the orginal id sent by the frontend
                    # Format for circle is [<center-pt>, <radius>]
                    changedEntities.append({"id": c["id"] - self._entityIdBase, "t": "circle", "v": [c["params"][1] - self._entityIdBase, radius]})
            return result, self.sys.Dof, changedEntities
        else:
            # result code + list of ids of failed constraints (corrected to the value sent by the frontend)
            return result, [elem - self._constraintIdBase for elem in self.sys.Failed], []
