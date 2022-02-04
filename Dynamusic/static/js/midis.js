function archivesPlay(filename){
    MIDIjs.stop();
    MIDIjs.play('../static/week_audio/' + filename + '.mid');
}