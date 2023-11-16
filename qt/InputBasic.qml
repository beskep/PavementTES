import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "custom"

Pane {
    function set_variables() {
        let data = {
            "water": {
                "cp": parseFloat(cp_water.text),
                "rho": parseFloat(rho_water.text),
                "porosity": parseFloat(porosity_water.text),
                "efficiency": parseFloat(efficiency_water.text) / 100
            },
            "sand": {
                "cp": parseFloat(cp_sand.text),
                "rho": parseFloat(rho_sand.text),
                "porosity": parseFloat(porosity_sand.text),
                "efficiency": parseFloat(efficiency_sand.text) / 100
            },
            "environment": {
                "delta_temperature": parseFloat(delta_temperature.text),
                "daily_radiation": parseFloat(daily_radiation.text)
            }
        };
        controller.set_basic_variable('water', JSON.stringify(data['water']));
        controller.set_basic_variable('sand', JSON.stringify(data['sand']));
        controller.set_basic_variable('environment', JSON.stringify(data['environment']));
    }

    function save_buttons() {
        cp_water.save();
        cp_sand.save();
        rho_water.save();
        rho_sand.save();
        porosity_water.save();
        porosity_sand.save();
        efficiency_water.save();
        efficiency_sand.save();
        delta_temperature.save();
        daily_radiation.save();
    }

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Button {
                text: '저장'
                highlighted: true
                Material.roundedScale: Material.SmallScale
                onReleased: {
                    save_buttons();
                    set_variables();
                }
            }

            Button {
                text: '초기화'
                highlighted: true
                Material.roundedScale: Material.SmallScale
                onReleased: {
                    cp_water.text = 4.2;
                    cp_sand.text = 0.9;
                    rho_water.text = 1000;
                    rho_sand.text = 2000;
                    porosity_water.text = 0.5;
                    porosity_sand.text = 0.5;
                    efficiency_water.text = 50;
                    efficiency_sand.text = 50;
                    delta_temperature.text = 30;
                    daily_radiation.text = 4.3;
                    save_buttons();
                }
            }

        }

        RowLayout {
            spacing: 10

            GroupBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: '물성치'

                GridLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.margins: 20
                    columns: 4
                    columnSpacing: 20

                    Rectangle {
                    }

                    Label {
                        text: '물'
                        font.bold: true
                    }

                    Label {
                        text: '모래'
                        font.bold: true
                    }

                    Rectangle {
                    }

                    // 정압비열
                    Label {
                        text: '정압비열 (Cp)'
                    }

                    TextFieldStatus {
                        id: cp_water

                        text: '4.2'

                        validator: DoubleValidator {
                        }

                    }

                    TextFieldStatus {
                        id: cp_sand

                        text: '0.9'

                        validator: DoubleValidator {
                        }

                    }

                    Label {
                        text: 'kJ/kg℃'
                    }

                    // 밀도
                    Label {
                        text: '밀도 (ρ)'
                    }

                    TextFieldStatus {
                        id: rho_water

                        text: '1000'

                        validator: DoubleValidator {
                        }

                    }

                    TextFieldStatus {
                        id: rho_sand

                        text: '2000'

                        validator: DoubleValidator {
                        }

                    }

                    Label {
                        text: 'kg/m³'
                    }

                    // 공극률
                    Label {
                        text: '공극률'
                    }

                    TextFieldStatus {
                        id: porosity_water

                        // FIXME 물만 있을 땐 공극률 적용 안됨
                        text: '0.5'

                        validator: DoubleValidator {
                        }

                    }

                    TextFieldStatus {
                        id: porosity_sand

                        text: '0.5'

                        validator: DoubleValidator {
                        }

                    }

                    Label {
                        text: '-'
                    }

                    // 열저장효율
                    Label {
                        text: '열저장효율'
                    }

                    TextFieldStatus {
                        id: efficiency_water

                        text: '50'

                        validator: DoubleValidator {
                        }

                    }

                    TextFieldStatus {
                        id: efficiency_sand

                        text: '50'

                        validator: DoubleValidator {
                        }

                    }

                    Label {
                        text: '%'
                    }

                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }

            }

            GroupBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: '환경변수'

                GridLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.margins: 20
                    columns: 3
                    columnSpacing: 20

                    // 온도차
                    Label {
                        text: '온도차'
                    }

                    TextFieldStatus {
                        id: delta_temperature

                        text: '30'

                        validator: DoubleValidator {
                        }

                    }

                    Label {
                        text: '℃'
                    }

                    // 일간평균일사량
                    Label {
                        text: '일간평균일사량'
                    }

                    TextFieldStatus {
                        id: daily_radiation

                        text: '4.3'

                        validator: DoubleValidator {
                        }

                    }

                    Label {
                        text: 'kWh/m²·day'
                    }

                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }

            }

        }

    }

}
