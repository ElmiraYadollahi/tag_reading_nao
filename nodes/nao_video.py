


def connectToCamera( self ):
        try:
            self.avd = ALProxy( "ALVideoDevice" )
            strMyClientName = self.getName()
            nCameraNum = 1
            nResolution = 1
            nColorspace = 0
            nFps = 5
            self.strMyClientName = self.avd.subscribeCamera( strMyClientName,
 								nCameraNum, nResolution, nColorspace, nFps )
        except BaseException, err :
            self.log( "ERR: connectToCamera: catching error: %s!" % err )

    def disconnectFromCamera( self ):
        try:
            self.avd.unsubscribe( self.strMyClientName )
        except BaseException, err:
            self.log( "ERR: disconnectFromCamera: catching error: %s!" % err )

def getImageFromCamera( self ):
        """
        return the image from camera or None on error
        """
        try:
            dataImage = self.avd.getImageRemote( self.strMyClientName )

            if( dataImage != None ):
                  Image = (
                           numpy.reshape(
                                 numpy.frombuffer(dataImage[6], dtype='%iuint8' % dataImage[2]), 
                                 (dataImage[1], dataImage[0], dataImage[2])
                                        )
                          )
              return image

        except BaseException, err:
            self.log( "ERR: getImageFromCamera: catching error: %s!" % err )
        return None;

