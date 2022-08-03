import { Bar } from './bar.js';
import { Donut } from './donut.js';

(function(){
	console.log( 'hello world!' )
	d3.json( '/load_data' ) // async
		.then( data => main( data ) ) // run the application
		.catch( err => console.error( err ) ) // print errors if there are any
		
	
})();

// Global Variables
function main( data ) {
	// Input to main
	d3.select( "#observations" )
		.append( "span" )
		.text( data.observations.length )

	let	bars = new Bar( 'vis1', data );
	let donut = new Donut( 'vis2', data );
}


function disableButtonState(elem) {
    if(confirm('Are you sure you want to disable this button?') == true) {
        elem.disabled = true;
        alert("its done.");
    }
    else {
        return false;
    }
}