from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox
from io import BytesIO
import os

class Stegno:
    art = '''
███████╗████████╗███████╗ ██████╗  █████╗ ███╗   ██╗ ██████╗ 
██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗████╗  ██║██╔═══██╗
███████╗   ██║   █████╗  ██║  ███╗███████║██╔██╗ ██║██║   ██║
╚════██║   ██║   ██╔══╝  ██║   ██║██╔══██║██║╚██╗██║██║   ██║
███████║   ██║   ███████╗╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝
╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                             '''
    art2 = '''
 ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗██╗   ██╗
██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║╚██╗ ██╔╝
██║  ███╗██████╔╝███████║██████╔╝███████║ ╚████╔╝ 
██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║  ╚██╔╝  
╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║   ██║   
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝   
                                                  
'''
    output_image_size = 0
    BG_COLOR = '#3A4526'  # Darker Olive Green
    TEXT_COLOR = '#F5F3E4'  # Off-White
    BUTTON_BG = '#F5F3E4'  # Off-White
    BUTTON_FG = '#B5784C'  # Burnt Orange
    SHADOW_COLOR = '#5A6B3D'  # Dark Olive Green

    def main(self, root):
        root.title('ImageSteganography')
        root.geometry('500x600')
        root.resizable(width=False, height=False)
        root.configure(bg=self.BG_COLOR)
        f = Frame(root, bg=self.BG_COLOR)

        title = Label(f, text='Image Steganography', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        title.config(font=('times new roman', 33))
        title.grid(row=0, pady=10, columnspan=2)

        button_frame = Frame(f, bg=self.BG_COLOR)
        button_frame.grid(row=1, pady=12, columnspan=2)

        self.create_rounded_button(button_frame, "Encode", lambda: self.frame1_encode(f), 0, 0)
        self.create_rounded_button(button_frame, "Decode", lambda: self.frame1_decode(f), 0, 1)

        ascii_art = Label(f, text=self.art, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        # Change the font size from 60 to a smaller value like 30 or 40
        ascii_art.config(font=('courier', 8, 'bold'))
        ascii_art.grid(row=2, pady=5, columnspan=2)

        ascii_art2 = Label(f, text=self.art2, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        ascii_art2.config(font=('courier', 8, 'bold'))
        ascii_art2.grid(row=3, pady=5, columnspan=2)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        f.grid()

    def create_rounded_button(self, parent, text, command, row, col):
        canvas = Canvas(parent, width=150, height=40, bg=self.BG_COLOR, highlightthickness=0)
        canvas.grid(row=row, column=col, padx=10)

        # Draw shadow
        canvas.create_rectangle(15, 15, 135, 35, fill=self.SHADOW_COLOR, outline=self.SHADOW_COLOR, tags="shadow")
        canvas.create_oval(10, 15, 30, 35, fill=self.SHADOW_COLOR, outline=self.SHADOW_COLOR, tags="shadow")
        canvas.create_oval(120, 15, 140, 35, fill=self.SHADOW_COLOR, outline=self.SHADOW_COLOR, tags="shadow")

        # Draw main button shape
        canvas.create_rectangle(15, 10, 135, 30, fill=self.BUTTON_BG, outline=self.BUTTON_BG, tags="button")
        canvas.create_oval(10, 10, 30, 30, fill=self.BUTTON_BG, outline=self.BUTTON_BG, tags="button")
        canvas.create_oval(120, 10, 140, 30, fill=self.BUTTON_BG, outline=self.BUTTON_BG, tags="button")

        canvas.create_text(75, 20, text=text, fill=self.BUTTON_FG, font=('courier', 14))
        
        canvas.bind("<Button-1>", lambda event: command())

    def home(self, frame):
        frame.destroy()
        self.main(root)

    def frame1_decode(self, f):
        f.destroy()
        d_f2 = Frame(root, bg=self.BG_COLOR)
        label_art = Label(d_f2, text='DECODER', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        label_art.config(font=('courier', 90))
        label_art.grid(row=1, pady=50)
        l1 = Label(d_f2, text='Select Image with Hidden text:', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        l1.config(font=('courier', 18))
        l1.grid()

        button_frame = Frame(d_f2, bg=self.BG_COLOR)
        button_frame.grid(pady=15)
        self.create_rounded_button(button_frame, "Select", lambda: self.frame2_decode(d_f2), 0, 0)
        self.create_rounded_button(button_frame, "Cancel", lambda: Stegno.home(self, d_f2), 0, 1)

        d_f2.grid()

    def frame2_decode(self, d_f2):
        d_f3 = Frame(root, bg=self.BG_COLOR)
        myfile = tkinter.filedialog.askopenfilename(filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l4 = Label(d_f3, text='Selected Image :', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
            l4.config(font=('courier', 18))
            l4.grid()
            panel = Label(d_f3, image=img, bg=self.BG_COLOR)
            panel.image = img
            panel.grid()
            hidden_data = self.decode(myimg)
            l2 = Label(d_f3, text='Hidden data is :', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
            l2.config(font=('courier', 18))
            l2.grid(pady=10)
            text_area = Text(d_f3, width=50, height=10, bg=self.BUTTON_BG, fg=self.BUTTON_FG)
            text_area.insert(INSERT, hidden_data)
            text_area.configure(state='disabled')
            text_area.grid()
            
            button_frame = Frame(d_f3, bg=self.BG_COLOR)
            button_frame.grid(pady=15)
            self.create_rounded_button(button_frame, "Cancel", lambda: self.page3(d_f3), 0, 0)

            d_f3.grid(row=1)
            d_f2.destroy()

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

    def frame1_encode(self, f):
        f.destroy()
        f2 = Frame(root, bg=self.BG_COLOR)
        label_art = Label(f2, text='ENCODER', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        label_art.config(font=('courier', 70))
        label_art.grid(row=1, pady=50)
        l1 = Label(f2, text='Select the Image in which \nyou want to hide text :', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        l1.config(font=('courier', 18))
        l1.grid()

        button_frame = Frame(f2, bg=self.BG_COLOR)
        button_frame.grid(pady=15)
        self.create_rounded_button(button_frame, "Select", lambda: self.frame2_encode(f2), 0, 0)
        self.create_rounded_button(button_frame, "Cancel", lambda: Stegno.home(self, f2), 0, 1)

        f2.grid()

    def frame2_encode(self, f2):
        ep = Frame(root, bg=self.BG_COLOR)
        myfile = tkinter.filedialog.askopenfilename(filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            myimg = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l3 = Label(ep, text='Selected Image', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
            l3.config(font=('courier', 18))
            l3.grid()
            panel = Label(ep, image=img, bg=self.BG_COLOR)
            panel.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            panel.grid()
            l2 = Label(ep, text='Enter the message', bg=self.BG_COLOR, fg=self.TEXT_COLOR)
            l2.config(font=('courier', 18))
            l2.grid(pady=15)
            text_area = Text(ep, width=50, height=10, bg=self.BUTTON_BG, fg=self.BUTTON_FG)
            text_area.grid()

            button_frame = Frame(ep, bg=self.BG_COLOR)
            button_frame.grid(pady=15)
            self.create_rounded_button(button_frame, "Encode", lambda: [self.enc_fun(text_area, myimg), Stegno.home(self, ep)], 0, 0)
            self.create_rounded_button(button_frame, "Cancel", lambda: Stegno.home(self, ep), 0, 1)

            ep.grid(row=1)
            f2.destroy()

    def info(self):
        try:
            str_info = 'original image:-\nsize of original image:{}mb\nwidth: {}\nheight: {}\n\n' \
                       'decoded image:-\nsize of decoded image: {}mb\nwidth: {}' \
                       '\nheight: {}'.format(self.output_image_size.st_size / 1000000,
                                             self.o_image_w, self.o_image_h,
                                             self.d_image_size / 1000000,
                                             self.d_image_w, self.d_image_h)
            messagebox.showinfo('Info', str_info)
        except:
            messagebox.showinfo('Info', 'Unable to get the information')

    def genData(self, data):
        newd = []
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)
        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_area, myimg):
        data = text_area.get("1.0", "end-1c")
        if (len(data) == 0):
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            my_file = BytesIO()
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]
            save_path = tkinter.filedialog.asksaveasfilename(initialfile=temp, filetypes=([('png', '*.png')]), defaultextension=".png")
            if save_path:
                newimg.save(save_path)
                self.d_image_size = os.stat(save_path).st_size
                self.d_image_w, self.d_image_h = newimg.size
                messagebox.showinfo("Success", f"Encoding Successful\nFile is saved as {os.path.basename(save_path)}")

    def page3(self, frame):
        frame.destroy()
        self.main(root)

root = Tk()
o = Stegno()
o.main(root)
root.mainloop()
