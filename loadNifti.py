def load_NIFTI(filePath):
    niftiIMG = nib.load(filePath)
    return niftiIMG

def getVoxelCoords(niftiIMG):
    data = niftiIMG.get_fdata()
    nonZero = np.argwhere(data>0)