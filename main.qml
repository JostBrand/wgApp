import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Window {
    id:root
    width: 1024
    height: 600
    maximumHeight : 600
    maximumWidth : 1024
    minimumHeight : 600
    minimumWidth : 1024
    visible: true
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
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/
