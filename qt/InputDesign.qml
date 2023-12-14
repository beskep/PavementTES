import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import "custom"

Pane {
    property var column_width: 250

    function _row(x) {
        return {
            "efficiency": x.efficiency / 100,
            "duration": x.duration,
            "area": x.area,
            "material": x.material
        };
    }

    function set_variables() {
        let rows = table_model.rows.map(_row);
        controller.set_design_variables(JSON.stringify(rows));
    }

    function add_row() {
        table_model.appendRow(table_model.rows[table_model.rowCount - 1]);
        set_variables();
    }

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Button {
                text: '추가'
                highlighted: true
                Material.roundedScale: Material.SmallScale
                onReleased: add_row()
            }

            Button {
                text: '초기화'
                highlighted: true
                Material.roundedScale: Material.SmallScale
                onReleased: {
                    table_model.rows = [{
                        "efficiency": '25.0',
                        "duration": '90.0',
                        "area": '10.0',
                        "material": 0
                    }];
                    set_variables();
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
                model: ['발전 효율', '인버터 효율', '컨트롤러 효율', '보정 방법']
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

                    rows: [{
                        "efficiency": '25.0',
                        "duration": '90.0',
                        "area": '10.0',
                        "material": 0
                    }]

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

                }

                delegate: DelegateChooser {
                    DelegateChoice {
                        column: 3

                        delegate: ComboBox {
                            implicitWidth: column_width
                            model: ['자동', '적용', '미적용']
                            currentIndex: display
                            onActiveFocusChanged: {
                                display = currentIndex;
                                set_variables();
                            }
                        }

                    }

                    DelegateChoice {

                        delegate: TextField {
                            implicitWidth: column_width
                            text: model.display
                            onEditingFinished: {
                                model.display = text;
                                set_variables();
                            }

                            validator: DoubleValidator {
                            }

                        }

                    }

                }

            }

        }

    }

}
