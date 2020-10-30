import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Page {

    Connections{
        target: Coffee

        onQmlTasksSignal:{
        console.log(groupId)
        console.log(taskString)

        calendarWeek.text = weekDates

        if(groupId == 1) {
                group1text.text = taskString
                group1namestext.text= "Jonas & Sharon"
                task1pic.source = picturePath
                if(checked){group1rect.color = "green"
                }
        }
        else if(groupId == 2) {
                group2text.text = taskString
                group2namestext.text= "Amir & Anja"
                task2pic.source = picturePath
                if(checked){group2rect.color = "green"}
        }
        else if(groupId == 3) {
                group3text.text = taskString
                group3namestext.text="Jarno & Miri"
                task3pic.source = picturePath
                if(checked){group3rect.color = "green"}
        }
        else if(groupId == 4) {
                group4text.text = taskString
                group4namestext.text="Alex & Jost & Kira"
                task4pic.source = picturePath
                if(checked){group4rect.color = "green"}
        }
        else if(groupId == 5) {
                group5text.text = taskString
                group5namestext.text= "Tij & Felix"
                task5pic.source = picturePath
                if(checked){group5rect.color = "green"}
            }

        if (taskString == "reload"){
            authWT.close()
            thankYouWT.open()
            thankyouTimerWT.start()
            grid.update()
        }
        }
    }
    Timer {
        id : thankyouTimerWT
        interval: 3000; running: false; repeat: false;
        onTriggered:{
            console.log("Closing Thank You Popup")
            thankYouWT.close()
        }
    }


    id: wTPage
    title: qsTr("wtPage")
    Image {
        id: imageWTpage
        anchors.fill: parent
        source: "Pictures/Tasks/backgroundTasks.jpg"
        fillMode: Image.PreserveAspectCrop

        Text {
            id: textimageWTpage
            width: 300
            height: 89
            color: "black"
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
            text: ""
            font.pixelSize: 12
            color: "#ffffff"
        }
    }
    Button {
        id: homebuttonWT
        x: parent.width-150-50
        y: parent.height*0.85
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



GridLayout {
    id: grid
    //anchors.fill: parent
    x: parent.width*0.05
    y: parent.height*0.1
    width: parent.width*0.9
    height: parent.height*0.70

    Popup {
                  id: authWT
                  parent: Overlay.overlay
                  x: Math.round((parent.width - width) / 2)
                  y: Math.round((parent.height - height) / 2)
                  width: parent.width/2
                  height: parent.height/2
                  modal: true
                  focus: true
                  closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
                  Image {
                      id: cleaningAuthImage
                      anchors.fill: parent
                      source: "Pictures/CleaningProcess.jpg"
                      fillMode: Image.PreserveAspectCrop
                  Label {
                      Text{
                          id:cleaningAuthImageText
                          text:"Please login with your RFID-Chip."
                          fontSizeMode: Text.Fit
                          font.pointSize: 20
                          }

                      }
                  }
          }//auth POPup

    Popup {
                  id: thankYouWT
                  parent: Overlay.overlay
                  x: Math.round((parent.width - width) / 2)
                  y: Math.round((parent.height - height) / 2)
                  width: parent.width/2
                  height: parent.height/2
                  modal: true
                  focus: true
                  closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
                  Image {
                      id: thankYouWTImage
                      anchors.fill: parent
                      source: "Pictures/CleaningProcess.jpg"
                      fillMode: Image.PreserveAspectCrop
                  Label {
                      Text{
                          id:thankYouWTText
                          text:"Thank you for fullfilling your duty."
                          fontSizeMode: Text.Fit
                          font.pointSize: 20
                          }

                      }
                  }
          }//auth POPup


    rows: 2
    columns: 3

    Rectangle {
         id: group1rect
         color: "red"
         border.width: 2
         Layout.fillHeight: true
         Layout.fillWidth: true
         Layout.columnSpan: 1
         Layout.rowSpan: 1
         Layout.row: 1
         Layout.column: 1

         MouseArea {
         anchors.fill: parent
         onClicked: {
         authWT.open() // emit the parent's signal
         Coffee.Auth("TaskStatus")
       } }

         Rectangle{
             color: "white"
             y: parent.height*0.2
             anchors.horizontalCenter: parent.horizontalCenter
             width: parent.width*0.95
             height: parent.height*0.785



             Image {
                 anchors.fill: parent
                 id: task1pic
                 source: ""
                 fillMode: Image.PreserveAspectCrop
                }
         }

         Text {
            id: group1text
            text: "task1"
            width: parent.width
            height: parent.height*0.3
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.Wrap
            font.pointSize: 15
         }

         Rectangle {
              id: group1names
              color: "white"
              border.width: 2
              anchors.bottom: parent.bottom
              anchors.bottomMargin: 0
              anchors.horizontalCenter: parent.horizontalCenter
              //x: parent.width*0.2
              y: parent.height*0.8
              width: parent.width*0.8
              height: parent.height*0.2


              Text {
                 id: group1namestext
                 text: ""
                 anchors.fill: parent
                 horizontalAlignment: Text.AlignHCenter
                 verticalAlignment: Text.AlignVCenter
                 //anchors.centerIn: parent
                 font.pointSize: 15
              }

         }

    }

    Rectangle {
        id: group2rect
         color: "red"
         border.width: 2
         Layout.fillHeight: true
         Layout.fillWidth: true
         Layout.columnSpan: 1
         Layout.rowSpan: 1
         Layout.row: 1
         Layout.column: 2

         MouseArea {
         anchors.fill: parent
         onClicked: {
         authWT.open() // emit the parent's signal
             Coffee.Auth("TaskStatus")

       } }

         Rectangle{
             color: "white"
             y: parent.height*0.2
             anchors.horizontalCenter: parent.horizontalCenter
             width: parent.width*0.95
             height: parent.height*0.785

             Image {
                 anchors.fill: parent
                 id: task2pic
                 source: ""
                 fillMode: Image.PreserveAspectCrop
                }
         }

         Text {
            id: group2text
            text: "task2"
            width: parent.width
            height: parent.height*0.3
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.Wrap
            font.pointSize: 15
         }
         Rectangle {
              id: group2names
              color: "white"
              border.width: 2
              anchors.bottom: parent.bottom
              anchors.bottomMargin: 0
              anchors.horizontalCenter: parent.horizontalCenter
              //x: parent.width*0.2
              y: parent.height*0.8
              width: parent.width*0.8
              height: parent.height*0.2


              Text {
                 id: group2namestext
                 text: ""
                 anchors.fill: parent
                 horizontalAlignment: Text.AlignHCenter
                 verticalAlignment: Text.AlignVCenter
                 //anchors.centerIn: parent
                 font.pointSize: 15
              }



         }
    }

    Rectangle {
        id: group3rect
         color: "red"
         border.width: 2
         Layout.fillHeight: true
         Layout.fillWidth: true
         Layout.columnSpan: 1
         Layout.rowSpan: 1
         Layout.row: 1
         Layout.column: 3

         MouseArea {
         anchors.fill: parent
         onClicked: {
         authWT.open() // emit the parent's signal
             Coffee.Auth("TaskStatus")

       } }

         Rectangle{
             color: "white"
             y: parent.height*0.2
             anchors.horizontalCenter: parent.horizontalCenter
             width: parent.width*0.95
             height: parent.height*0.785

             Image {
                 anchors.fill: parent
                 id: task3pic
                 source: ""
                 fillMode: Image.PreserveAspectCrop
                }
         }

         Text {
            id: group3text
            text: "task3"
            width: parent.width
            height: parent.height*0.3
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.Wrap
            font.pointSize: 15
         }
         Rectangle {
              id: group3names
              color: "white"
              border.width: 2
              anchors.bottom: parent.bottom
              anchors.bottomMargin: 0
              anchors.horizontalCenter: parent.horizontalCenter
              //x: parent.width*0.2
              y: parent.height*0.8
              width: parent.width*0.8
              height: parent.height*0.2


              Text {
                 id: group3namestext
                 text: ""
                 anchors.fill: parent
                 horizontalAlignment: Text.AlignHCenter
                 verticalAlignment: Text.AlignVCenter
                 //anchors.centerIn: parent
                 font.pointSize: 15
              }


         }
    }

    Rectangle {
        id: group4rect
         color: "red"
         border.width: 2
         Layout.fillHeight: true
         Layout.fillWidth: true
         Layout.columnSpan: 1
         Layout.rowSpan: 1
         Layout.row: 2
         Layout.column: 1

         MouseArea {
         anchors.fill: parent
         onClicked: {
         authWT.open() // emit the parent's signal
             Coffee.Auth("TaskStatus")

       } }

         Rectangle{
             color: "white"
             y: parent.height*0.2
             anchors.horizontalCenter: parent.horizontalCenter
             width: parent.width*0.95
             height: parent.height*0.785

             Image {
                 anchors.fill: parent
                 id: task4pic
                 source: ""
                 fillMode: Image.PreserveAspectCrop
                }
         }

         Text {
            id: group4text
            text: "task4"
            width: parent.width
            height: parent.height*0.3
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.Wrap
            font.pointSize: 15
         }
         Rectangle {
              id: group4names
              color: "white"
              border.width: 2
              anchors.bottom: parent.bottom
              anchors.bottomMargin: 0
              anchors.horizontalCenter: parent.horizontalCenter
              //x: parent.width*0.2
              y: parent.height*0.8
              width: parent.width*0.8
              height: parent.height*0.2

              Text {
                 id: group4namestext
                 text: ""
                 anchors.fill: parent
                 horizontalAlignment: Text.AlignHCenter
                 verticalAlignment: Text.AlignVCenter
                 //anchors.centerIn: parent
                 font.pointSize: 15
              }

         }
    }

    Rectangle {
        id: group5rect
         color: "red"
         border.width: 2
         Layout.fillHeight: true
         Layout.fillWidth: true
         Layout.columnSpan: 1
         Layout.rowSpan: 1
         Layout.row: 2
         Layout.column: 2

         MouseArea {
         anchors.fill: parent
         onClicked: {
         authWT.open() // emit the parent's signal
             Coffee.Auth("TaskStatus")

       } }

         Rectangle{
             color: "white"
             y: parent.height*0.2
             anchors.horizontalCenter: parent.horizontalCenter
             width: parent.width*0.95
             height: parent.height*0.785

             Image {
                 anchors.fill: parent
                 id: task5pic
                 source: ""
                 fillMode: Image.PreserveAspectCrop
                }
         }

         Text {
            id: group5text
            text: "task5"
            width: parent.width
            height: parent.height*0.3
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.Wrap
            font.pointSize: 15
         }
         Rectangle {
              id: group5names
              color: "white"
              border.width: 2
              anchors.bottom: parent.bottom
              anchors.bottomMargin: 0
              anchors.horizontalCenter: parent.horizontalCenter
              //x: parent.width*0.2
              y: parent.height*0.8
              width: parent.width*0.8
              height: parent.height*0.2


              Text {
                 id: group5namestext
                 text: ""
                 anchors.fill: parent
                 horizontalAlignment: Text.AlignHCenter
                 verticalAlignment: Text.AlignVCenter
                 //anchors.centerIn: parent
                 font.pointSize: 15
              }

         }
    }
    Rectangle {
        id: summaryrect
         color: "white"
         border.width: 2
         Layout.fillHeight: true
         Layout.fillWidth: true
         Layout.columnSpan: 1
         Layout.rowSpan: 1
         Layout.row: 2
         Layout.column: 3

         Text {
            id: summarytext
            text: "summary"
            width: parent.width
            height: parent.height*0.3
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.Wrap
            font.pointSize: 15
         }

    }
}


} //Page

/*##^##
Designer {
    D{i:0;autoSize:true;height:600;width:1024}
}
##^##*/
