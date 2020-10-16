import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Page {

    title: qsTr("frontPage")
    Image {
        id: imageWT
        x: root.width/2
        y: 0
        width: root.width/2
        height: root.height
        source: "Pictures/WgTasksMain.jpg"
        fillMode: Image.PreserveAspectCrop

        MouseArea {
            id: mouseAreaWT
            acceptedButtons: Qt.LeftButton
            anchors.fill: parent
            onClicked: {
                console.log("WT pressed");
                swipeView.setCurrentIndex(2)
                }
        }
    }

    Image {
        id: imageCoffe
        x: 0
        y: 0
        width: root.width/2
        height: root.height
        source: "Pictures/coffeeMainPage.jpg"
        fillMode: Image.PreserveAspectCrop

        MouseArea {
            id: mouseAreaCoffee
            anchors.fill: parent
            onClicked: {
                 console.log("Coffee pressed");
                swipeView.setCurrentIndex(1) }
        }
    }

    Rectangle {
        id: rectangleTextBottom
        x: 0
        y: 549
        width: root.width
        height: 51
        color: "#000000"
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0

        Text {
            id: textCoffee
            x: root.width/4-width
            y: 0
            width: 261
            height: 51
            color: "#ffffff"
            text: qsTr("Coffee")
            anchors.bottom: parent.bottom
            font.pixelSize: 35
            horizontalAlignment: Text.AlignHCenter
            anchors.bottomMargin: 0
            font.bold: true
            minimumPixelSize: 35
        }

        Text {
            id: textWT
            x: root.width*3/4
            y: 0
            width: 261
            height: 51
            color: "#ffffff"
            text: qsTr("Weekly Tasks")
            anchors.bottom: parent.bottom
            font.pixelSize: 35
            horizontalAlignment: Text.AlignHCenter
            anchors.bottomMargin: 0
            font.bold: true
            minimumPixelSize: 35
        }
    }
}
