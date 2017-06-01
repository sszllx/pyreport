#include <QtCore>
#include <QDebug>
#include <QSharedPointer>

#include "downloader.h"
#include "extractor.h"

static void create_idfile(QString filename)
{
  QFile infile(filename);
  QString out_filename;
  int id_count = 0;

  out_filename = filename.replace(".log", ".id");
  QFile outfile(out_filename);
  QTextStream out(&outfile);

  if (!infile.open(QIODevice::ReadOnly | QIODevice::Text)) {
      qDebug() << "infile open failed";
      return;
  }

  if (!outfile.open(QIODevice::WriteOnly | QIODevice::Text)) {
      qDebug() << "outfile open failed";
      return;
  }

  while (!infile.atEnd()) {
    QString data = infile.read(4096);
    int index = 0;
    int totalLen = data.size();

    while ((index = data.indexOf("idfa", index)) > 0) {
      if (index + 42 >= totalLen) {
        index = totalLen - index;
        int pos = infile.pos();
        infile.seek(pos - index - 2);
        break;
      }

      index += 7;

      QString id = data.mid(index, 36);
      out << id << "\n";

      const char *ch = id.toStdString().c_str();

      printf("%d %s", id_count++, ch);
      printf("\r\033[k");
    }
  }
}

int main(int argc, char *argv[])
{
  QCoreApplication app(argc, argv);

  // QSharedPointer<Downloader> downloader(new Downloader);

//  create_idfile("");

//  Extractor e;
//  e.start_extract();

  qDebug() << "finish!";

  return app.exec();
}
