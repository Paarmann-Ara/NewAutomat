
# --
# ...
# --


class TestCompleteTools():

    @staticmethod
    def IsSupported(n, m):
        ...

# --
# ...
# --

    @staticmethod
    def GetAntwortFromAntwortList(Item, List):

        try:

            for it in List:
                if it[1] == Item:
                    return it[0]
            else:
                return 'Nothing'

        except Exception as exp:
            print(__name__ + ": " + str(exp))
# --
# ...
# --

    @staticmethod
    def FindLastItemPositionInContextMenu(ContextMenu):

        try:
            returnValue = None

            if cObjectToolbox.IsSupported(ContextMenu, 'Height'):
                returnValue = [12, ContextMenu.Height - 12]
            ContextMenu = None
            return returnValue

        except Exception as exp:
            print(__name__ + ": " + str(exp))
# --
# ...
# --

    @staticmethod
    def FindFirstItemPositionInContextMenu(ContextMenu):

        try:
            returnValue = None

            if cObjectToolbox.IsSupported(ContextMenu, 'Height'):
                returnValue = [10, 5]
            ContextMenu = None
            return returnValue

        except Exception as exp:
            print(__name__ + ": " + str(exp))
# --
# ...
# --

    @staticmethod
    def ChangeListViewVerticalScrollPosition(ListViewObject, AddPosition):

        try:

            if ListViewObject is None or ListViewObject == 'nothing' or not cObjectToolbox.IsSupported(ListViewObject, 'Exists'):
                return
            elif not ListViewObject.Exists or not cObjectToolbox.IsSupported(ListViewObject, 'VScroll'):
                return

            temp = ListViewObject.VScroll.Pos + AddPosition
            if temp < ListViewObject.VScroll.Max:
                ListViewObject.VScroll.Pos = temp
            else:
                ListViewObject.VScroll.Pos = ListViewObject.VScroll.Max
            ListViewObject = None

        except Exception as exp:
            print(__name__ + ": " + str(exp))
# --
# ...
# --

    @staticmethod
    def ChangeListViewHorisantalScrollPosition(ListViewObject, AddPosition):

        try:

            if ListViewObject is None or ListViewObject == 'nothing' or not cObjectToolbox.IsSupported(ListViewObject, 'Exists'):
                return
            elif not ListViewObject.Exists or not cObjectToolbox.IsSupported(ListViewObject, 'HScroll'):
                return

            temp = ListViewObject.HScroll.Pos + AddPosition
            if temp < ListViewObject.HScroll.Max:
                ListViewObject.HScroll.Pos = temp
            else:
                ListViewObject.HScroll.Pos = ListViewObject.HScroll.Max
            ListViewObject = None

        except Exception as exp:
            print(__name__ + ": " + str(exp))
# --
# ...
# --

    @staticmethod
    def ResetListViewScrollPosition(ListViewObject):

        try:

            if ListViewObject is None or ListViewObject == 'nothing' or not cObjectToolbox.IsSupported(ListViewObject, 'Exists'):
                return

            elif not ListViewObject.Exists or not cObjectToolbox.IsSupported(ListViewObject, 'HScroll'):
                return

            ListViewObject.HScroll.Pos = 0

        except Exception as exp:
            print(__name__ + ": " + str(exp))
