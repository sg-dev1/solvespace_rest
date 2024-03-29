import slvs

# Taken from slvs.h
SLVS_RESULT_OKAY=0
SLVS_RESULT_INCONSISTENT=1
SLVS_RESULT_DIDNT_CONVERGE=2
SLVS_RESULT_TOO_MANY_UNKNOWNS=3

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
        self._entityIdBase = 100
        self._constraintIdBase = 1

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
        return planeId

    def addPoint(self, plane, idHint, data):
        planeId = self._planeStrToPlaneId(plane)

        # TODO either here we must select the proper points (according to plane) or the frontend needs to do it

        p1Id = self._paramId
        self.sys.addParam(slvs.makeParam(p1Id, self.solveGroup, data[0]))
        self._paramId = self._paramId + 1
        p2Id = self._paramId
        self.sys.addParam(slvs.makeParam(p2Id, self.solveGroup, data[1]))
        self._paramId = self._paramId + 1
        #p3Id = self._paramId
        #self.sys.addParam(slvs.makeParam(p3Id, self.solveGroup, data[2]))
        #self._paramId = self._paramId + 1
        #self.sys.addEntity(slvs.makePoint3d(idHint + self._entityIdBase, self.solveGroup, planeId, p1Id, p2Id, p3Id))

        print("make point with id %d and coords (%.3f, %.3f, %.3f)" % (idHint, data[0], data[1], data[2]))

        self.sys.addEntity(slvs.makePoint2d(idHint + self._entityIdBase, self.solveGroup, planeId, p1Id, p2Id))

    def addLine(self, plane, idHint, data):
        planeId = self._planeStrToPlaneId(plane)

        print("add line with id %d and data %s" % (idHint, str(data)))

        self.sys.addEntity(
            slvs.makeLineSegment(idHint + self._entityIdBase, self.solveGroup, planeId, data[0] + self._entityIdBase, data[1] + self._entityIdBase)
            )
    
    def addConstraint(self, plane, idHint, constraintType, data):
        planeId = self._planeStrToPlaneId(plane)

        print("add constraint with id %d and type %d and data %s" % (idHint, constraintType, str(data)))

        valA = data[0]
        ptA = 0
        if data[1] != 0:
            ptA = data[1] + self._entityIdBase
        ptB = 0
        if data[2] != 0:
            ptB = data[2] + self._entityIdBase
        entityA = 0
        if data[3] != 0:
            entityA = data[3] + self._entityIdBase
        entityB = 0
        if data[4] != 0:
            entityB = data[4] + self._entityIdBase

        print("\t%.3f, %d, %d, %d, %d" % (valA, ptA, ptB, entityA, entityB))

        self.sys.addConstraint(
            slvs.makeConstraint(idHint + self._constraintIdBase, self.solveGroup, constraintType, planeId, valA, ptA, ptB, entityA, entityB)
            )

    def solve(self):
        result = self.sys.solve(self.solveGroup, True)

        if result == SLVS_RESULT_OKAY:
            # TODO parse the changed coordinates
            changedEntities = []
            return result, self.sys.Dof, changedEntities
        else:
            # result code + list of ids of failed constraints
            return result, self.sys.Failed, []
