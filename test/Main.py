import wx
import random
from Board import *

global tile_scale

class Main(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(400, 400))

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('0')
        self.board = BoardContainer(self)
        self.board.SetFocus()

        self.Centre()
        self.Show(True)
        
class BoardContainer(wx.Panel):
    BoardWidth = 20
    BoardHeight = 20
#    Speed = 300
    ID_TIMER = 1

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)

        global tile_scale
        tile_scale = 16

#        self.timer = wx.Timer(self, Board.ID_TIMER)

        self.game = Game()
        game = self.game
#        game.play(1, pieces['5W'], 1, 0, [0,0])
#        game.play(2, pieces['5V'], 1, 0, [17,0])
#        game.play(3, pieces['5V'], 2, 0, [17,17])
#        game.play(4, pieces['5V'], 3, 0, [0,17])
#        game.play(1, pieces['5I'], 0, 0, [3,3])
        
        self.curPiece = 0
        self.curX = 0
        self.curY = 0
        self.curR = 0
        self.curFlip = 0

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
#        self.Bind(wx.EVT_TIMER, self.OnTimer, id=Board.ID_TIMER)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        
        game = self.game
        
        size = self.GetClientSize()
        for i in range(len(game.board)):
            for j in range(len(game.board)):
#                shape = self.shapeAt(j, Board.BoardHeight - i - 1)
#                if shape != Tetrominoes.NoShape:
                    self.drawSquare(dc,
                        0 + j * tile_scale,
                        0 + i * tile_scale, game.board[j][i])

#        if self.curPiece.shape() != Tetrominoes.NoShape:
        p = pieces[pieces.keys()[self.curPiece]]
        p = rotPiece(p, self.curR)
        if self.curFlip:
            p = flipPiece(p)
        
        for i in range(len(p)):
            ix = self.curX + p[i][0]
            iy = self.curY + p[i][1]
            self.drawSquare(dc, 0 + ix * tile_scale,
                0 + iy * tile_scale,
                game.curr_turn)

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()

#        if keycode == ord('P') or keycode == ord('p'):
#            self.pause()
#            return
#        if self.isPaused:
#            return
        if keycode == wx.WXK_LEFT:
            self.curX -= 1
        elif keycode == wx.WXK_RIGHT:
            self.curX += 1
        elif keycode == wx.WXK_DOWN:
            self.curY += 1
        elif keycode == wx.WXK_UP:
            self.curY -= 1
        elif keycode == ord('Z'):
            self.curR -= 1
            self.curR &= 3
        elif keycode == ord('X'):
            self.curR += 1
            self.curR &= 3
        elif keycode == ord('C'):
            self.curFlip ^= 1
        elif keycode == ord('A'):
            self.curPiece -= 1
            self.curPiece %= len(pieces)
        elif keycode == ord('S'):
            self.curPiece += 1
            self.curPiece %= len(pieces)
        elif keycode == wx.WXK_SPACE:
            piece_key = pieces.keys()[self.curPiece]
            player = self.game.curr_turn
            
            
            if self.game.hasPiece(player, piece_key):
                success = self.game.play(player, piece_key, self.curR, self.curFlip, [self.curX,self.curY])
                if success:
                    self.game.curr_turn += 1
                    if self.game.curr_turn > 4:
                        self.game.curr_turn = 1
        else:
            event.Skip()
        
        self.Refresh()
#
#
#    def OnTimer(self, event):
#        if event.GetId() == Board.ID_TIMER:
#            if self.isWaitingAfterLine:
#                self.isWaitingAfterLine = False
#                self.newPiece()
#            else:
#                self.oneLineDown()
#        else:
#            event.Skip()

    def drawSquare(self, dc, x, y, shape):
        colors = ['#000000', '#CC6666', '#66CC66', '#6666CC',
                  '#CCCC66', '#CC66CC', '#66CCCC', '#DAAA00']

        light = ['#000000', '#F89FAB', '#79FC79', '#7979FC', 
                 '#FCFC79', '#FC79FC', '#79FCFC', '#FCC600']

        dark = ['#000000', '#803C3B', '#3B803B', '#3B3B80', 
                 '#80803B', '#803B80', '#3B8080', '#806200']

        pen = wx.Pen(light[shape])
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)

        dc.DrawLine(x, y + tile_scale - 1, x, y)
        dc.DrawLine(x, y, x + tile_scale - 1, y)

        darkpen = wx.Pen(dark[shape])
        darkpen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(darkpen)

        dc.DrawLine(x + 1, y + tile_scale - 1,
            x + tile_scale - 1, y + tile_scale - 1)
        dc.DrawLine(x + tile_scale - 1, 
        y + tile_scale - 1, x + tile_scale - 1, y + 1)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(colors[shape]))
        dc.DrawRectangle(x + 1, y + 1, tile_scale - 2, 
        tile_scale - 2)


app = wx.App(redirect = 0)
Main(None, -1, 'Blokus')
app.MainLoop()
