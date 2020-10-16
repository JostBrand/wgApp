import QtQuick 2.13
import QtQuick.Window 2.13
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Window {
    id:root
    width: 1024
    height: 600
    visible: true
    title: qsTr("Selbstverwirklichung")
    Connections{target:Coffee
    }
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
