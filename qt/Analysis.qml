import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtCharts
import Qt.labs.platform
import Qt.labs.qmlmodels

Pane {
    property alias chart_view: chart_view
    property alias table_view: table_view

    function set_chart_bars(text) {
        let values = JSON.parse(text);
        bar_set.values = values;
        xaxis.categories = Array.from({
            "length": values.length
        }, (_, i) => '#' + (i + 1));
        yaxis.min = 0;
        yaxis.max = Math.round(1.2 * Math.max.apply(null, values));
    }

    function set_table(text) {
        table_model.rows = JSON.parse(text);
    }

    ColumnLayout {
        anchors.fill: parent

        Button {
            text: '보고서 저장'
            highlighted: true
            Material.roundedScale: Material.SmallScale
            onReleased: file_dialog.open()
        }

        Pane {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ChartView {
                id: chart_view

                anchors.fill: parent
                titleFont.family: 'Source Han Sans KR'
                titleFont.pointSize: 18
                legend.visible: false
                // title: '저장 탱크 용량'
                antialiasing: true

                BarSeries {
                    BarSet {
                        id: bar_set

                        label: 'capacity'
                        values: [1]
                    }

                    axisX: BarCategoryAxis {
                        id: xaxis

                        labelsFont.family: 'Source Han Sans KR'
                        labelsFont.pointSize: 14
                        categories: ['#1']
                    }

                    axisY: ValueAxis {
                        id: yaxis

                        labelsFont.family: 'Source Han Sans KR'
                        labelsFont.pointSize: 14
                        min: 0
                        titleText: "저장 탱크 용량 (m³)"
                    }

                }

            }

        }

        Pane {
            Layout.fillWidth: true
            Layout.fillHeight: true

            HorizontalHeaderView {
                id: horizontal_header

                anchors.left: table_view.left
                anchors.top: parent.top
                syncView: table_view
                clip: true
                model: ['집열 효율', '집열 기간 (일)', '도로 면적 (m²)', '축열재', '축열량 (kJ)', '축열조 용량 (m³)']
            }

            VerticalHeaderView {
                id: vertical_header

                anchors.top: table_view.top
                anchors.left: parent.left
                syncView: table_view
                clip: true
            }

            TableView {
                id: table_view

                anchors.left: vertical_header.right
                anchors.top: horizontal_header.bottom
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                columnSpacing: 1
                rowSpacing: 1
                boundsBehavior: Flickable.StopAtBounds
                clip: true

                model: TableModel {
                    id: table_model

                    TableModelColumn {
                        display: 'efficiency'
                    }

                    TableModelColumn {
                        display: 'duration'
                    }

                    TableModelColumn {
                        display: 'area'
                    }

                    TableModelColumn {
                        display: 'material'
                    }

                    TableModelColumn {
                        display: 'heat'
                    }

                    TableModelColumn {
                        display: 'capacity'
                    }

                }

                delegate: Rectangle {
                    implicitWidth: 200
                    implicitHeight: 50

                    Text {
                        text: display
                        anchors.centerIn: parent
                        font.pointSize: 14
                    }

                }

            }

        }

    }

    FileDialog {
        id: file_dialog

        nameFilters: ['Excel 문서 (*.xlsx)']
        fileMode: FileDialog.SaveFile
        onAccepted: controller.write_table(file)
    }

}
