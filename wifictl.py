import wifi

class Wifictl:
    def Search(self):
        wifilist = []

        cells = wifi.Cell.all('wlan0')

        for cell in cells:
            wifilist.append(cell)

        return wifilist


    def Connect(self, ssid, password=None):
        wifilist = self.Search()
        for cell in wifilist:
            if cell.ssid == ssid:
                return cell
            return False

        if cell:
            savedcell =  wifi.Scheme.find('wlan0', ssid)


            # Already Saved from Setting
            if savedcell:
                savedcell.activate()
                return cell

            # First time to conenct
            else:
                if cell.encrypted:
                    if password:
                        scheme = Add(cell, password)

                        try:
                            scheme.activate()

                        # Wrong Password
                        except wifi.exceptions.ConnectionError:
                            Delete(ssid)
                            return False

                        return cell
                    else:
                        return False
                else:
                    scheme = Add(cell)

                    try:
                        scheme.activate()
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False

                    return cell
        
        return False


    def Add(self, cell, password=None):
        if not cell:
            return False

        scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
        scheme.save()
        return scheme


    def Delete(self, ssid):
        if not ssid:
            return False

        cell = FindFromSavedList(ssid)

        if cell:
            cell.delete()
            return True

        return False


if __name__ == '__main__':
    '''
    # Search WiFi and return WiFi list
    print Search()

    # Connect WiFi with password & without password
    print Connect('OpenWiFi')
    print Connect('ClosedWiFi', 'password')

    # Delete WiFi from auto connect list
    print Delete('DeleteWiFi')
    '''
