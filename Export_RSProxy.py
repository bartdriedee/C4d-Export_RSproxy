import c4d, redshift
from c4d import documents
import os

def ExportProxy():
    # Find the Redshift Proxy Export plugin
    plug = c4d.plugins.FindPlugin(redshift.Frsproxyexport, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        raise RuntimeError("Pluging not found")
        return False

    # Send MSG_RETRIEVEPRIVATEDATA to the plugin to retrieve the state
    op = {}
    if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
        return False

    # BaseList2D object stored in "imexporter" key holds the settings
    if "imexporter" not in op:
        return False
    imexporter = op["imexporter"]

    # Override export range.
    # For the full list of parameters take a look at frsproxyexport.h in the plugin res folder
    #imexporter[c4d.REDSHIFT_PROXYEXPORT_OBJECTS] = c4d.REDSHIFT_PROXYEXPORT_OBJECTS_ALL
    #imexporter[c4d.REDSHIFT_PROXYEXPORT_ANIMATION_RANGE] = c4d.REDSHIFT_PROXYEXPORT_ANIMATION_RANGE_MANUAL
    #imexporter[c4d.REDSHIFT_PROXYEXPORT_ANIMATION_FRAME_START] = 1
    #imexporter[c4d.REDSHIFT_PROXYEXPORT_ANIMATION_FRAME_END] = 2

    # Single frame export
    imexporter[c4d.REDSHIFT_PROXYEXPORT_ANIMATION_RANGE] = c4d.REDSHIFT_PROXYEXPORT_ANIMATION_RANGE_CURRENT_FRAME

    # Keep the default beauty config in the proxy. Used primarily when exporting entire scenes for rendering with the redshiftCmdLine tool
    imexporter[c4d.REDSHIFT_PROXYEXPORT_AOV_DEFAULT_BEAUTY]	= False

    # Don't need lights in our proxies
    imexporter[c4d.REDSHIFT_PROXYEXPORT_EXPORT_LIGHTS] = False

    # Automatic object replacement with proxies
    # Proxy contents will be offset around the selection cetner
    imexporter[c4d.REDSHIFT_PROXYEXPORT_OBJECTS] = c4d.REDSHIFT_PROXYEXPORT_OBJECTS_SELECTION
    imexporter[c4d.REDSHIFT_PROXYEXPORT_ORIGIN] = c4d.REDSHIFT_PROXYEXPORT_ORIGIN_WORLD #REDSHIFT_PROXYEXPORT_ORIGIN_OBJECTS for Boundingbox

    imexporter[c4d.REDSHIFT_PROXYEXPORT_AUTOPROXY_CREATE] = False
    imexporter[c4d.REDSHIFT_PROXYEXPORT_REMOVE_OBJECTS] = False

    doc = documents.GetActiveDocument()

    # Export each selected object as a separate proxy
    sel = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    if len(sel)==0:
        raise RuntimeError("Nothing selected")
        return False

    document_path = doc.GetDocumentPath()
    #proxy_path = "{0}{1}PROXIES".format(document_path,os.path.sep)

    if not document_path:
        raise RuntimeError('Save project before exporting objects')
        return False

    #if not os.path.exists(proxy_path):
    #    os.makedirs(proxy_path)

    for obj in sel:
        doc.SetSelection(obj)

        path = '{0}/proxy_{1}.rs'.format(document_path, obj.GetName().replace("_proxy","").replace("_Proxy",''))
        #path = '{0}/proxy_{1}.rs'.format(proxy_path, obj.GetName().replace("_proxy","").replace("_Proxy",''))
        print("Exporting %s" %path)
        c4d.documents.SaveDocument(doc, path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, redshift.Frsproxyexport)

    return True


if __name__=='__main__':
    ExportProxy()