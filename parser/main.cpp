#include <QtCore>
#include <QDebug>

const char filename[4][32] = {
                              "1.mobile.log",
                              "3.mobile.log",
                              "5.mobile.log",
                              "7.mobile.log"};

static void create_idfile(QString filename)
{
  QFile infile(filename);
  QString out_filename;
  int id_count = 0;

  out_filename = filename.replace(".log", ".id");
  QFile outfile(out_filename);
  QTextStream out(&outfile);

  // TODO: check failed
  infile.open(QIODevice::ReadOnly | QIODevice::Text);
  outfile.open(QIODevice::WriteOnly | QIODevice::Text);

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
      out << id << "\n";//data << "\n\n\n\n\n\n+++++++++++++++++++++++++\n\n\n\n";

      const char *ch = id.toStdString().c_str();

      printf("%d %s", id_count++, ch);
      printf("\r\033[k");
    }
  }
}

void check()
{
  QStringList files;

  files << "1.mobile.id";
  files << "3.mobile.id";
  files << "5.mobile.id";
  files << "7.mobile.id";

  foreach(QString item, files) {
    QFile file(item);
    qDebug() << "check" << item;

    file.open(QIODevice::ReadOnly | QIODevice::Text);
    while (!file.atEnd()) {
      QString line = file.readLine();
      if (line.size() != 37) {
        qDebug() << "error!  " << line << line.size();
        return;
      }
    }
  }
}

int main(int argc, char *argv[])
{
  QCoreApplication app(argc, argv);

  if (argc > 1 && strcmp(argv[1], "check") == 0) {
    check();
    return 0;
  }

  int file_num = 4;
  int index;

  for (index = 0; index < file_num; index++) {
    create_idfile(filename[index]);
  }

  qDebug() << "finish!";

  return app.exec();
}
