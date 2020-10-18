import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Page {

//    Connections{
//        target: Coffee
//        onSliderSignal: {
//            console.log("func")
//            homebuttonWTtext.text = "hans"

//        }
//   }

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
        y: parent.height*0.9
        Text{id:homebuttonWTtext
            text:"Home"
            fontSizeMode: Text.Fit
            anchors.centerIn: parent
            font.pointSize: 18
        }
        anchors.bottom: parent.bottom
        anchors.rightMargin: 5
        anchors.bottomMargin: 20
        width: 150
        height: 50

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
        width: parent.width*0.7
        height: parent.height*0.7
        color: "#ffffff"

        Component {
            id: tasksDelegate
            Item {
                width: parent.width; height: parent.width/8
                Column {
                    Text { text: '<b>Name:</b> ' + name }
                    Text { text: '<b>Number:</b> ' + number }
                }
            }
        }

        ListView {
            anchors.fill:parent
            highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
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
