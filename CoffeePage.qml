import QtQuick 2.13
import QtQuick.Window 2.13
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Page {
    title: qsTr("coffePage")
    Image {
        id: imageCoffePage
        anchors.fill: parent
        source: "Pictures/CoffePage.jpg"
        fillMode: Image.PreserveAspectCrop

        ProgressBar {
            id: control
            x: 0
            y: 0
            width: parent.width
            height: parent.width*0.02
            value: 0.5
            padding: 2

            background: Rectangle {
                implicitWidth: parent.width
                implicitHeight: 6
                color: "#e6e6e6"
                radius: 3
            }

            contentItem: Item {
                implicitWidth: 200
                implicitHeight: 4

                Rectangle {
                    width: control.visualPosition * parent.width
                    height: parent.height
                    radius: 2
                    color: "#663300"
                }
            }

            Label {
                id: coffeBeansTextLabel
                x: parent.x
                y: parent.height*1.1
                width: 240
                height: 50
                color: "#ffffff"
                text: qsTr("Coffee Beans")
                font.pointSize: 29
            }
        }
        Button {
            id: homebuttonCoffee
            x: parent.width-150-50
            y: parent.height*0.9
            Text{
                id:homebuttonCoffeeText
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

        Button {
            id: buttonCleaning
            x: parent.width-150-50
            y: parent.height*0.1
            width: 150
            height: 50

            background: Rectangle {
                anchors.fill:parent
                color: "white"
                border.width: 1
                border.color: "black"
                radius: 8
            }

            Text{
                id:buttonCleaningText
                text:"Cleaning"
                fontSizeMode: Text.Fit
                anchors.centerIn: parent
                font.pointSize: 18
            }
            anchors.right: parent.right
            anchors.rightMargin: 50
            onClicked: { cleaningProcess.open()}
        }

        Button {
            id: buttonStartCoffe
            x:parent.width/2-200/2
            y: parent.height*0.8
            width: parent.width/5
            height:parent.height/6


            background: Rectangle {
                anchors.fill:parent
                id: bgbuttonStartCoffe
                color: "white"
                border.width: 1
                border.color: "black"
                radius: 8
            }

            Text{
                id:buttonStartCoffeText
                text:"Start"
                fontSizeMode: Text.Fit
                anchors.centerIn: parent
                font.pointSize: 25
            }

            onClicked: {
                payingProcess.open()
            }
        }
        Popup {
                id: cleaningProcess
                parent: Overlay.overlay
                x: Math.round((parent.width - width) / 2)
                y: Math.round((parent.height - height) / 2)
                width: 800
                height: 700
                modal: true
                focus: true
                closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
                Image {
                    id: cleaningProcessImage
                    anchors.fill: parent
                    source: "Pictures/CleaningProcess.jpg"
                    fillMode: Image.PreserveAspectCrop
                Label {
                    Text{
                        id:cleaningProcessText
                        text:"Starting the cleaning process"
                        fontSizeMode: Text.Fit
                        font.pointSize: 18

                    }

                }
                }
        }

        Popup {
                id: payingProcess
                parent: Overlay.overlay
                x: Math.round((parent.width - width) / 2)
                y: Math.round((parent.height - height) / 2)
                width: 800
                height: 700
                modal: true
                focus: true
                closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
                Image {
                    id: payingProcessImage
                    anchors.fill: parent
                    source: "Pictures/Payment.jpg"
                    fillMode: Image.PreserveAspectCrop
                Label {

                    text: qsTr("Please hold your NFC chip near to the reader")
                }

                }
        }

    }
}

/*##^##
Designer {
    D{i:0;height:600;width:1024}D{i:2}
}
##^##*/
