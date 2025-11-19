const { app, BrowserWindow } = require('electron')

function createWindow(){
    const win = new BrowserWindow({
        // Window size
        width: 1500,
        height: 1500,
        resizable: true,
        webPreference: {
            nodeIntegration: true
        }
    })
    win.loadFile(__dirname + "/html/index.html")
    // win.webContents.openDevTools()
}    
    
app.whenReady().then(createWindow)

app.on("window-all-closed", () => {
        app.quit()
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})