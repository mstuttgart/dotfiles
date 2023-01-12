/**
 * GNOME Shell extenstion to hide the Activities button from the status bar.
 *
 * Created by Shay Elkin <shay@shayel.org>
 *
 * Updated by zeten30@gmail.com
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 *
 **/

const Main = imports.ui.main;
let monitorsChangedEvent = null;

function hideIndicator() {
    let indicator = Main.panel.statusArea['activities'];
    if(indicator != null) {
        indicator.hide();
    }
}

function enable() {
    monitorsChangedEvent = Main.layoutManager.connect('monitors-changed', hideIndicator);
    hideIndicator();
}

function disable() {
    Main.layoutManager.disconnect(monitorsChangedEvent);
    let indicator = Main.panel.statusArea['activities'];
    if(indicator != null) {
        indicator.show();
    }
}
