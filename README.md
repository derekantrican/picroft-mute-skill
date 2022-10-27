# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/microphone-slash.svg" card_color="#E69138" width="50" height="50" style="vertical-align:bottom"/> Picroft Mute
Adds support for a mute button to picroft

## About
Adds support for a mute button to picroft using the gpio pins. You can either say one of the mute phrases (such as "Mycroft, mute" or "Mycroft, stop listening") or push the button to toggle mute.

Currently, this skill is NOT customizable, but will be in the future. It is strictly set up for the below configuration:

- Button: BOARD pin 10 (**NOTE: this mycroft skill is not set up for a regular push button, but for a [toggle button](https://www.adafruit.com/product/1683)**)
- LED: BOARD pin 12

![](https://i.imgur.com/Nge0pfE.png)

## Future plans for customization:

- Pin number for the button
- Pin number for the LED
- Whether the LED "on" represents "muted" or "unmuted"
- Whether the button is a simple push button or a toggle button

## Credits
Derek Antrican (@derekantrican)

## Category
**IoT**
Media
Productivity

## Tags
#Picroft
#Mute
#Button
#Gpio
#Mycroft

