import slvs

class Slvs_Helper():
    def __init__(self):
        self.sys = slvs.System()
        self.workPlaneGroup = 1
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
