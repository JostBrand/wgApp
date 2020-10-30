import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Controls.Imagine 2.3
import QtQuick.Extras 1.4

Page {

    Connections{
        target: Coffee

	onQmlBeansSignal:{sliderBeans.value = emitBeansValue}

	onQmlBalanceSignal:{ popupRefillThankYouText.text = "Thank you. \n Your new balance is:" + emitBalanceValue
		console.log("thankyou text set")}

    onQmlRfidSignal:{
                console.log("onQmlRfidSignal")
                if (emitRfidTag != "")
                 {
                    if (payingProcess.activeFocus)
                    {
                        payingProcess.close()
                    }
                    if (cleaningAuth.activeFocus)
                    {
                        cleaningAuth.close()
                        cleaningProcess.open()
                    }
                    if (popupRefill.activeFocus)
                    {
                        popupRefill.close()
                        popupRefillConfirm.open()
                    }
                }
    }
    onQmlReadySignal:{
        if (emitReadyValue == false){
            readyCircle.color = "red"
        }
        else{
            readyCircle.color = "green"
        }
    }
    }

    title: qsTr("coffePage")
    Image {
        id: imageCoffePage
        anchors.fill: parent
        source: "Pictures/CoffePage.jpg"
        fillMode: Image.PreserveAspectCrop

        ProgressBar {
            id: sliderBeans
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
                    width: sliderBeans.visualPosition * parent.width
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

        Rectangle {
         id: readyCircle
         x: parent.width*0.02
         y: parent.height*0.95
         width: 30
         height: 30
         color: "red"
         border.color: "black"
         border.width: 1
         radius: width*0.5
         Text {
              anchors.fill: parent
              color: "red"
              text: " "
         }
    }
		Button {
					id: refundButton
					x: parent.width*0.1
					y: parent.height*0.9
					Text{
						id:refundButtonText
						text:"Refund"
						fontSizeMode: Text.Fit
						anchors.centerIn: parent
						font.pointSize: 18
					}
					anchors.bottom: parent.bottom
					anchors.rightMargin: 5
					anchors.bottomMargin: 20
					width: 200
					height: 100

					background: Rectangle {
						anchors.fill:parent
						color: "white"
						border.width: 1
						border.color: "black"
						radius: 8
					}

					onClicked: {
								Coffee.refund()
								readyCircle.color = "blue"
					}
		}//RefundButton

        Button {
            id: homebuttonCoffee
            x: parent.width*0.8
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
            width: 200
            height: 100

            background: Rectangle {
                anchors.fill:parent
                color: "white"
                border.width: 1
                border.color: "black"
                radius: 8
            }

            onClicked: {
                        swipeView.setCurrentIndex(0)
                        Coffee.closeReadBeans()
                    	}
        }//homebuttonCoffee

        Button {
            id: buttonRefill
            x: parent.width*0.8
            y: parent.height*0.25
            width: 200
            height: 100

            background: Rectangle {
                anchors.fill:parent
                color: "white"
                border.width: 1
                border.color: "black"
                radius: 8
            }

            Text{
                id:buttonRefillText
                text:"Refill"
                fontSizeMode: Text.Fit
                anchors.centerIn: parent
                font.pointSize: 18
			}
            onClicked: {
                        Coffee.Auth("Refill")
						popupRefill.open()
                        }
        }//buttonRefill

		Popup {
                id: popupRefill
                parent: Overlay.overlay
                x: Math.round((parent.width - width) / 2)
                y: Math.round((parent.height - height) / 2)
                width: parent.width/2
                height: parent.height/2
                modal: true
                focus: true
                closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
                Image {
						id: popupRefillImage
						anchors.fill: parent
						source: "Pictures/RefillConfirm.jpg"
						fillMode: Image.PreserveAspectCrop
					Label {
							Text{
								id:popupRefillImageText
								text:"Please login with your RFID-Chip."
								color:"white"
								fontSizeMode: Text.Fit
								font.pointSize: 20
							}
					}

				}
        }

		Popup {
                id: popupRefillConfirm
                parent: Overlay.overlay
                x: Math.round((parent.width - width) / 2)
                y: Math.round((parent.height - height) / 2)
                width: parent.width/2
                height: parent.height/2
                modal: true
                focus: true
                closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
                Image {
                    id: popupRefillConfirmImg
                    anchors.fill: parent
                    source: "Pictures/RefillConfirm.jpg"
                    fillMode: Image.PreserveAspectCrop
                Label {
					x: parent.width*0.1
					y: parent.height*0.2
                    Text{
                        id:popupRefillConfirmText
                        text:"Please confirm."
						color:"white"
                        fontSizeMode: Text.Fit
                        font.pointSize: 30
					}
				}

			Button {
				id: popupRefillConfirmYes
				x: parent.width*0.05
				y: parent.height/2
				width: 200
				height: 100

				background: Rectangle {
					anchors.fill:parent
					color: "white"
					border.width: 1
					border.color: "black"
					radius: 8
				}

				Text{
					id:popupRefillConfirmYesText
					text:"Yes"
					fontSizeMode: Text.Fit
					anchors.centerIn: parent
					font.pointSize: 25
				}
				onClicked: {
							popupRefillConfirm.close()
							popupRefillThankYou.open()
							timerThankYou.start()
							Coffee.confirmRefill()
							}
			}

			Button {
				id: popupRefillConfirmNo
				x:parent.width*0.55
				y: parent.height/2
				width: 200
				height: 100

				background: Rectangle {
					anchors.fill:parent
					color: "white"
					border.width: 1
					border.color: "black"
					radius: 8
				}

				Text{
					id:popupRefillConfirmNoText
					text:"No"
					fontSizeMode: Text.Fit
					anchors.centerIn: parent
					font.pointSize: 25
				}

				onClicked: {
					popupRefillConfirm.close()
				}
			}
        }
    }

		Timer {
			id : timerThankYou
			interval: 3000; running: false; repeat: false;
			onTriggered:{
				console.log("Closing Thank You Popup")
				popupRefillThankYou.close()
			}
		}

		Popup {
                id: popupRefillThankYou
                parent: Overlay.overlay
                x: Math.round((parent.width - width) / 2)
                y: Math.round((parent.height - height) / 2)
                width: parent.width/2
                height: parent.height/2
                modal: true
                focus: true
                closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside



                Image {
						id: popupRefillThankYouImg
						anchors.fill: parent
						source: "Pictures/RefillConfirm.jpg"
						fillMode: Image.PreserveAspectCrop
					Label {
					x: parent.width*0.025
					y: parent.height*0.2
						Text{
							id:popupRefillThankYouText
							text:"please fill me up ;)"
							color:"white"
							fontSizeMode: Text.Fit
							font.pointSize: 25
							}
						}
        		}
		}

        Button {
            id: buttonCleaning
            x: parent.width*0.8
            y: parent.height*0.1
            width: 200
            height: 100

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
            onClicked: {
                        cleaningAuth.open()
                        Coffee.Auth("Cleaning")
                        }
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
                payingProcess.open() //Open Paying Popup window
                Coffee.Auth("Coffee")
            }
        }
	Popup {
                id: cleaningAuth
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
        }

	Popup {
                id: cleaningProcess
                parent: Overlay.overlay
                x: Math.round((parent.width - width) / 2)
                y: Math.round((parent.height - height) / 2)
                width: parent.width/2
                height: parent.height/2
                modal: true
                focus: true
                closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

                Image {
                    id: cleaningProcessImage
                    anchors.fill: parent
                    source: "Pictures/CleaningProcess.jpg"
                    fillMode: Image.PreserveAspectCrop
                        Label {
                            Text{
                                id:cleaningProcessText
                                text:"Cleaning type:"
                                fontSizeMode: Text.Fit
								color: "white"
                                font.pointSize: 20
                                }
                            }
                //buttons
                Button {
                    id: buttonPopupMilk
                    x: parent.width*0.1
                    y: parent.height*0.1
                    width: 200
                    height: 100

                    background: Rectangle {
                        anchors.fill:parent
                        color: "white"
                        border.width: 1
                        border.color: "black"
                        radius: 8
                    }

                    Text{
                        id:buttonPopupMilkText
                        text:"Milk"
                        fontSizeMode: Text.Fit
                        anchors.centerIn: parent
                        font.pointSize: 18
                    }
                    onClicked: { Coffee.cleaningMilk()
                                cleaningProcess.close()
                    }
                }
                Button {
                    id: buttonPopupLime
                    x: parent.width*0.1
                    y: parent.height*0.4
                    width: 200
                    height: 100

                    background: Rectangle {
                        anchors.fill:parent
                        color: "white"
                        border.width: 1
                        border.color: "black"
                        radius: 8
                    }

                    Text{
                        id:buttonPopupLimeText
                        text:"Lime"
                        fontSizeMode: Text.Fit
                        anchors.centerIn: parent
                        font.pointSize: 18
                    }
                    onClicked: { cleaningFullPopup.open()
                                 cleaningProcess.close()
                                 //Coffee.setCleaningLime()
								Coffee.setter("cleaningType","Lime")
                                 }
                }
                Button {
                    id: buttonPopupFull
                    x: parent.width*0.1
                    y: parent.height*0.7
                    width: 200
                    height: 100

                    background: Rectangle {
                        anchors.fill:parent
                        color: "white"
                        border.width: 1
                        border.color: "black"
                        radius: 8
                    }

                    Text{
                        id:buttonPopupFullText
                        text:"Full"
                        fontSizeMode: Text.Fit
                        anchors.centerIn: parent
                        font.pointSize: 18
                    }
                    onClicked: { cleaningFullPopup.open()
                                 cleaningProcess.close()
                                 //Coffee.setCleaningFull()
								 Coffee.setter("cleaningType","Full")
						}
                }
            }
        }
        Popup {
                id: cleaningFullPopup
                parent: Overlay.overlay
                x: Math.round((parent.width - width) / 2)
                y: Math.round((parent.height - height) / 2)
                width: parent.width/2
                height: parent.height/2
                modal: true
                focus: true
                closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
                Image {
                    id: cleaningProcessImageFullPopup
                    anchors.fill: parent
                    source: "Pictures/CleaningProcess.jpg"
                    fillMode: Image.PreserveAspectCrop
                Label {
                    Text{
                        id:cleaningProcessFullPopupText
                        text:"Cleaning type:"
                        fontSizeMode: Text.Fit
                        font.pointSize: 14
                        }

                    }
                //buttons
                Button {
                    id: cleaningFullPopupStart
                    x: parent.width*0.1
                    y: parent.height*0.2
                    width: 200
                    height: 100

                    background: Rectangle {
                        anchors.fill:parent
                        color: "white"
                        border.width: 1
                        border.color: "black"
                        radius: 8
                    }

                    Text{
                        id:cleaningFullPopupStartText
                        text:"Run"
                        fontSizeMode: Text.Fit
                        anchors.centerIn: parent
                        font.pointSize: 18
                    }
                    onClicked: {
                                 Coffee.press_start()
                                 Coffee.cleaningCounter = Coffee.cleaningCounter +1
                    }
                }
                Button {
                    id: cleaningFullPopupFinish
                    x: parent.width*0.1
                    y: parent.height*0.45
                    width: 200
                    height: 100

                    background: Rectangle {
                        anchors.fill:parent
                        color: "white"
                        border.width: 1
                        border.color: "black"
                        radius: 8
                    }

                    Text{
                        id:cleaningFullPopupFinishText
                        text:"Finish"
                        fontSizeMode: Text.Fit
                        anchors.centerIn: parent
                        font.pointSize: 18
                    }
                    onClicked: {
                                cleaningFullPopup.close()
                                 Coffee.incCleaning()
                                 Coffee.cleaningCouter = 0
                    }
                }
                }
        }

        Popup {
                id: payingProcess
                parent: Overlay.overlay
                x: Math.round((parent.width - width) / 2)
                y: Math.round((parent.height - height) / 2)
                width: parent.width/2
                height: parent.height/2
                modal: true
                focus: true

                closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
                Image {
                    id: payingProcessImage
                    anchors.fill: parent
                    source: "Pictures/Payment.jpg"
                    fillMode: Image.PreserveAspectCrop

					Rectangle {
						width: parent.width
						height: parent.height/4
						radius: 2
						color: "white"
						Label {
							fontSizeMode: Text.Fit
							text: qsTr("Please hold your NFC chip near to the reader")
						}
					}
                }
                onClosed: {
                    Coffee.closeRfidThread()
					          Coffee.setBalanceText()
                    popupRefillThankYou.open()
                    timerThankYou.start()
                }
        }

    }
}

/*##^##
Designer {
    D{i:0;height:600;width:1024}D{i:2}
}
##^##*/
