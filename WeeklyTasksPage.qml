import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Page {

    id: wTPage
    title: qsTr("wtPage")
    Image {
        id: imageWTpage
        anchors.fill: parent
        source: "Pictures/WgTasksPage.jpg"
        fillMode: Image.PreserveAspectCrop

        Text {
            id: textimageWTpage
            width: 300
            height: 89
            color: "#ffffff"
            text: qsTr("Weekly Tasks")
            font.pixelSize: 45
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: calendarWeek
            x: parent.width-150-50
            y: 54
            width: 226
            height: 28
            text: qsTr("calWeek")
            font.pixelSize: 12
            color: "#ffffff"
        }
    }
    Button {
        id: homebuttonWT
        x: parent.width-150-50
        y: parent.height*0.8
        Text{id:homebuttonWTtext
            text:"Home"
            fontSizeMode: Text.Fit
            anchors.centerIn: parent
            font.pointSize: 18
        }
        width: 200
        height: 100

        background: Rectangle {
            anchors.fill:parent
            color: "white"
            border.width: 1
            border.color: "black"
            radius: 8
        }

        onClicked: { swipeView.setCurrentIndex(0)}
    }

    Rectangle {
        id: rectangleTextBottom
        anchors.centerIn: parent
        width: parent.width
        height: parent.height*0.7
        color: "transparent"


        Component {
            id: tasksDelegate
            Item {

                Column {
                    anchors.centerIn: parent
                    anchors.fill:parent
                    Button {
                        anchors.centerIn: parent
                        background: Rectangle {
                            anchors.fill:parent
                            color: "white"
                            border.width: 1
                            border.color: "black"
                            radius: 1
                        }
                        Text{id:homebuttonWTtext
                            text: '<b>Name:</b> ' + name + '\n' + '<b>Number:</b> ' + number
                            fontSizeMode: Text.Fit
                            anchors.centerIn: parent
                            font.pointSize: 10
                        }

                    }

                }
            }
        }

        GridView {
            id: view
            x: 194
            y: 24
            width: parent.width; height: parent.height
            cellWidth: 400; cellHeight: 150

            model: WgTasks {}
            delegate: tasksDelegate
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:600;width:1024}
}
##^##*/
