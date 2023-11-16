import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

TextField {
    property string original_foreground: '#dd000000'

    function save() {
        Material.foreground = original_foreground;
        if (text[0] === '*')
            text = text.slice(1);

    }

    Layout.preferredWidth: 175
    Component.onCompleted: {
        original_foreground = Material.foreground;
    }
    onTextEdited: {
        Material.foreground = '#606060';
        if (text[0] !== '*')
            text = '*' + text;

    }
}
