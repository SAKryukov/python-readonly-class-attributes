class PropertySet:
    @property
    def readOnlyValue(self):
        return 13
    readWriteValue = 14

propertyDemo = PropertySet()
print (PropertySet.readOnlyInt)
print (propertyDemo.readOnlyValue)
propertyDemo.readOnlyValue = 100 # will throw exception
