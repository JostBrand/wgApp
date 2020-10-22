import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Window {
    id:root
    width: 1024
    height: 768
    maximumHeight : 768
    maximumWidth : 1024
    minimumHeight : 768
    minimumWidth : 1024
    visible: true
    visibility: Window.FullScreen

    title: qsTr("Selbstverwirklichung")

    Connections{target:Coffee}

    SwipeView {
        id: swipeView
        anchors.fill: parent
        currentIndex: 0
        Component.onCompleted: contentItem.interactive = false

        FrontPage{}
        CoffeePage{}
        WeeklyTasksPage{}

    }
    Shortcut {
        sequence: "Esc"
        onActivated: root.close()}
    }

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/
