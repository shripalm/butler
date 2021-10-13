const vr = require("voice-recognition");
const recognizer = new vr("en-IN");
recognizer.continuos = false;
recognizer.sameThread = true;
recognizer.listen();
recognizer.on( "vc:detected", ( audio ) => {
    console.log( audio );
})