import urlhandler
import pygtk
pygtk.require('2.0')
import gtk
import webkit
import gobject
from datetime import datetime
class Browser:
    f = open("Home", "r")
    f2 = f.read()
    f3 = f2.split("\n")
    default_site = f3[0]
    f.close()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        
        gobject.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_title('Blade Browser')
        self.window.set_size_request(800, 600)
        self.web_view = webkit.WebView()
        self.web_view.open(self.default_site)
        self.web_view.get_settings().set_property("enable-developer-extras",True)  
        toolbar = gtk.Toolbar()
        fav_list = gtk.ListStore(str)
        f = open("Favorites", "r")
        fav = f.read()
        f.close()
        favorites = fav.split("\n") 
        for favor in favorites:
            fav_list.append([favor])

        self.box1 = gtk.ComboBox(fav_list)
        self.box1.connect("changed", self.favorites_onchange)
        renderer_text = gtk.CellRendererText()
        self.box1.pack_start(renderer_text, True)
        self.box1.add_attribute(renderer_text, "text", 0)
        self.back_button = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.back_button.connect("clicked", self.go_back)

        self.forward_button = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.forward_button.connect("clicked", self.go_forward)

        refresh_button = gtk.ToolButton(gtk.STOCK_REFRESH)
        refresh_button.connect("clicked", self.refresh)
        def activate_inspector(self, *args):
            view = webkit.WebView()
            panels.add2(view)
            panels.set_position(panels.get_allocation().height / 2)
            view.show()
            return view
        quittb = gtk.ToolButton(gtk.STOCK_QUIT)
        ins = gtk.ToolButton(gtk.STOCK_PROPERTIES)
        nt = gtk.ToolButton(gtk.STOCK_ADD)
        fav = gtk.ToolButton(gtk.STOCK_PREFERENCES)
        hb = gtk.ToolButton(gtk.STOCK_HOME)
        toolbar.add(hb)
        toolbar.add(self.back_button)
        toolbar.add(self.forward_button)
        toolbar.add(refresh_button)        
        toolbar.add(nt)
        toolbar.add(fav)
        toolbar.add(ins)
        
        toolbar.add(quittb)
        newtab_bar = gtk.Toolbar()
        c = gtk.ToolButton()
        newtab_bar.add(c)
        quittb.connect("clicked", gtk.main_quit)
        ins.connect("clicked", self.settings)
        nt.connect("clicked", self.add)
        fav.connect("clicked", self.add_fav)
        hb.connect("clicked", self.home)
        self.url_bar = gtk.Entry()
        self.url_bar.connect("activate", self.on_active)

        self.web_view.connect("load_committed", self.update_buttons)

        scroll_window = gtk.ScrolledWindow(None, None)
        scroll_window.add(self.web_view)
        
        
        vbox = gtk.VBox(False, 0)
        vbox.pack_start(toolbar, False, True, 0)
        vbox.pack_start(self.url_bar, False, True, 0)
        #vbox.pack_start(newtab_bar, False, True, 0)
        vbox.pack_start(self.box1, False, False, 0)
        vbox.add(scroll_window)
        panels = gtk.VPaned()
        panels.add1(vbox)
        panels.show_all()
        self.window.add(panels)
        self.window.show_all()
        settings = self.web_view.get_settings()
        settings.set_property("enable-developer-extras", True)
        
        inspector = self.web_view.get_web_inspector()
        inspector.connect("inspect-web-view", activate_inspector)
        self.add(panels)
    def favorites_onchange(self, widge, data=None):
        tree_iter = self.box1.get_active_iter()
        if tree_iter != None:
            model = self.box1.get_model()
            url = model[tree_iter][0]
            self.web_view.open(url)    
    def add_fav(self, widge, data=None):  
        f = open("Favorites", "r+")
        f2 = f.read()
        f.seek(0)
        f.write(self.url_bar.get_text() + "\n" + f2)
        f.close()
    def home(self, widge, data=None):
        f = open("Home", "r")
        f2 = f.read()
        f3 = f2.split("\n")
        f.close()
        if f3[0] == 'home':
            f = open("Home.html", "r")
            f2 = f.read()
            f.close()
            self.web_view.load_html_string(f2, "")
        else:    
            self.web_view.open(f3[0])
                
    def settings(self, widge, data=None):
            f = open("Settings.html", "r")
            self.web_view.load_html_string("<h1>Blade Settings:</h1>" + f.read(), '')
            f.close()        
    def on_active(self, widge, data=None):
        url = self.url_bar.get_text()
        if "blade://history" in url:
            if url == "blade://history?clear":
                f = open("History.html", "w")
                f.write("")
                self.web_view.load_html_string("<body onload='alert(" + '"Your History Has Been Cleared!")' + "'></body>", '')
                f.close()  
            elif url == "blade://history?clear=fav":   
                f = open("Favorites", "w")
                f.write("")
                self.web_view.load_html_string("<body onload='alert(" + '"Your Favorites Have Been Cleared!")' + "'></body>", '')
                f.close()  
            else:    
                f = open("History.html", "r")
                self.web_view.load_html_string("<h1>Blade History:</h1>" + f.read(), '')
                f.close()
            
        else:    
            if "." in url:
                try:
                    url.index("://")
                except:
                    url = "http://" + url
            else:
                url = "https://www.google.com/?gws_rd=ssl#q=" + url
            c = urlhandler.urlhandler(url)
            c.openURL()
            d = c.getURLdata()
            d2 = d.split("\n")
            #d2[0] == "# text/python"
            if ".py" in url:
                exec(d)
            c.closeURL()
            self.web_view.open(url)
            f = open("History.html", "a+")
            i = datetime.now()
            f.write("<br>" + "<a href='" + url + "'>" + url + "</a> At: " + i.strftime('%Y/%m/%d %H:%M:%S'))
            f.close()
        try:    
            d3 = d.split("<title>")
            d4 = d3[1].split("</title>")
            title = d4[0]
        except:
            title = url
        self.window.set_title('Blade Browser - %s' % title)    
        self.url_bar.set_text(url)
    def add(self, widget, data=None):  
        print "This feature doesn't exist yet!"
        
    def inspect(self, widge, data=None):
        url = self.url_bar.get_text()
        inspect = gtk.Window()
        inspect.set_position(gtk.WIN_POS_CENTER)
        inspect.set_size_request(400, 200)
        inspect.set_title("Inspect Element - %s" % url)
        scroller = gtk.ScrolledWindow()
        c = urlhandler.urlhandler(url)
        c.openURL()
        d = c.getURLdata()
        e = d.replace(">", ">\n")
        f = e.replace("}", "}\n")
        c.closeURL()
        #print f
        vbox = gtk.VBox(False, 0)
        inspect.add(vbox)
        vbox.show()
        #entry2 = gtk.Label(f)
        view = webkit.WebView()  
        view.open(url)
        view.get_settings().set_property("enable-developer-extras",True)  
        inspector = view.get_settings().get_dom_document()
        #buffer1.set_text(f)
        vbox.pack_start(scroller)
        vbox.pack_start(view, True, True, 0)
        view.show()
        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()
        inspect.show()    

    
    def go_back(self, widget, data=None):
        self.web_view.go_back()

    def go_forward(self, widget, data=None):
        self.web_view.go_forward()

    def refresh(self, widget, data=None):
        self.web_view.reload()

    def update_buttons(self, widget, data=None):
        self.url_bar.set_text( widget.get_main_frame().get_uri() )
        self.back_button.set_sensitive(self.web_view.can_go_back())
        self.forward_button.set_sensitive(self.web_view.can_go_forward())

    def main(self):
        gtk.main()

if __name__ == "__main__":
    browser = Browser()
    browser.main()
