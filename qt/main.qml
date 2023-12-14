import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import "custom"

ApplicationWindow {
    property var tab_width: 150
    property alias basic: input_basic
    property alias design: input_design
    property alias analysis: analysis

    function page(p) {
        if (p === 'basic')
            return input_basic;
        else if (p === 'design')
            return input_design;
        else if (p === 'analysis')
            return analysis;
        else
            throw p;
    }

    width: 1600
    height: 900
    visible: true
    title: 'HVAC'

    FontLoader {
        source: '../assets/SourceHanSansKR-Normal.otf'
    }

    RowLayout {
        anchors.fill: parent

        VerticalTabBar {
            id: tab_bar

            Layout.preferredWidth: tab_width
            Layout.fillHeight: true

            TabButton {
                width: tab_width
                text: '기본 변수 입력'
            }

            TabButton {
                width: tab_width
                text: '대안 설정'
            }

            TabButton {
                width: tab_width
                text: '대안 분석'
            }

        }

        StackLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true
            currentIndex: tab_bar.currentIndex
            onCurrentIndexChanged: {
                if (currentIndex === 2)
                    input_design.set_variables();

            }

            InputBasic {
                id: input_basic
            }

            InputDesign {
                id: input_design
            }

            Analysis {
                id: analysis
            }

        }

    }

}
