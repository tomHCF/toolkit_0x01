'use strict';

var openSys = Module.findExportByName(null, 'open');
var writeSys = Module.findExportByName(null, 'write');
var closeSys = Module.findExportByName(null, 'close');
var readSys = Module.findExportByName(null, 'read');
var unlinkSys = Module.findExportByName(null, 'unlink');

function sendLog(sendMsg) {
	send({name: 'log', log_: sendMsg});
} 
function sendFile(sendMsg) {
	send({name: 'file'}, sendMsg);
}

Interceptor.attach(openSys, {
	onEnter: function (args) {
		
		this.pathname = Memory.readCString(args[0]);
		var flags = args[1].toInt32();
		sendLog("[*] open() onEnter : pathname: " + this.pathname + ", flag: " + flags);
	},
	onLeave: function (retval) {
	
		var fileDescriptor = retval.toInt32();
		sendLog("[*] open() onLeave : pathname: " + this.pathname + ", descriptor: " + fileDescriptor);
	}
});

Interceptor.attach(writeSys, {
	onEnter: function (args) {
		
		this.fileDescriptor  = args[0].toInt32();
		var buf = args[1];
		var count = args[2].toInt32();
		sendLog("[*] write() onEnter : descriptor: " + this.fileDescriptor + ", byte to write: " + count);
		sendLog("[*] buff: \n" + hexdump(buf, {length: count}));
		if(Memory.readCString(buf, 3) == "dex") {
			sendFile(Memory.readByteArray(buf, count));	
		}
	},
	onLeave: function (retval) {
	
		var number = retval.toInt32();
		sendLog("[*] write() onLeave : descriptor: " + this.fileDescriptor + ", written bytes: " + number);
	}
});

Interceptor.attach(closeSys, {
	onEnter: function (args) {
		
		var fileDescriptor  = args[0].toInt32();
		sendLog("[*] close() onEnter : descriptor: " + fileDescriptor);
	},
	onLeave: function (retval) {}
});

Interceptor.attach(unlinkSys, {
	onEnter: function (args) {
		
		var pathname = Memory.readCString(args[0]);
		sendLog("[*] unlink() onEnter : pathnamer: " + pathname);
	},
	onLeave: function (retval) {}
});

Interceptor.attach(readSys, {
	onEnter: function (args) {
		
		this.fileDescriptor  = args[0].toInt32();
		this.buf = args[1];
		this.count = args[2].toInt32();
		sendLog("[*] read() onEnter : descriptor: " + this.fileDescriptor + ", byte to write: " + this.count);
	},
	onLeave: function (retval) {
		sendLog("[*] buff: \n" + hexdump(this.buf, {length: this.count}));
	}
});
