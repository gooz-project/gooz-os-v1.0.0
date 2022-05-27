from os import statvfs
import gc

def mem_state():
    message = ""
    gc.collect()
    
    _statvfs = statvfs("/")
    
    total_blocks = _statvfs[1] * _statvfs[2]
    free_blocks = _statvfs[1] * _statvfs[3]
    
    total_blocks = float("{:.3f}".format(total_blocks/1048576))
    free_blocks = float("{:.3f}".format(free_blocks/1048576))
    
    message += "\nTotal ROM Size: "+str(total_blocks)+"MB\n"
    message += "Used ROM Size: "+str(total_blocks-free_blocks)+"MB\n"
    message += "Free ROM Size: "+str(free_blocks)+"MB\n"
    message += "ROM Usage Percentage: "+"{:.2f}".format(((total_blocks-free_blocks)/total_blocks)*100)+"%\n"
    
    free_ram = float("{:.3f}".format(gc.mem_free()/1024))  
    used_ram = float("{:.3f}".format(gc.mem_alloc()/1024)) 
    total_ram = free_ram + used_ram
    
    message += "\nTotal RAM Size: "+str(total_ram)+"KB\n"
    message += "Used RAM Size: "+str(used_ram)+"KB\n"
    message += "Free RAM Size: "+str(free_ram)+"KB\n"
    message += "RAM Usage Percentage: "+"{:.2f}".format((used_ram/total_ram)*100)+"%\n"
    return message
