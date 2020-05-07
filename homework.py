import datetime as dt


class Calculator:
   def __init__(self, limit):
        """Общая функциональность дочерних классов Calories- и CashCalculator.

        Свойства класса Calculator:
        -число limit (дневной лимит трат/калорий, который задал пользователь);
        -пустой список record(хранение записей).
        """
        
        self.limit = limit
        self.records = []
   def add_record(self, record):
      """Сохранение новой записи о расходах/приёме пищи.

      Метод принимает объект
      класса Record и сохраняет его в списке records.
      """
      self.records.append(record)
      
   def get_today_stats(self):
      """Сколько сегодня килокалорий получено/денег потрачено."""
      total = 0
      for record in self.records:
         if record.date == dt.datetime.now().date():
            total += record.amount
      return total

   def get_week_stats(self):
      """Сколько килокалорий получено/денег потрачено за последние 7 дней"""          
      now = dt.datetime.now().date()
      week_ago = now - dt.timedelta(days=6)
      total = 0
      for record in self.records:
         if week_ago <= record.date <= now:
            total += record.amount
      return total

                
class CaloriesCalculator(Calculator):
    """Дочерний класс класса Calculator.

    Добавленный метод -
    определение, сколько кКал ёще можно получить сегодня.
    """
    
    def get_calories_remained(self):
        """Сколько ещё калорий можно/нужно получить сегодня."""        
        remain = self.limit - self.get_today_stats()
        if remain > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remain} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Дочерний класс класса Calculator.

    Добавленный метод - информация о дневном балансе.
    """
    
    USD_RATE = 72.73
    EURO_RATE = 79.12
    
    def get_today_cash_remained(self, currency):
        """Возвращение сообщения о состоянии дневного баланса."""
        remain = self.limit - self.get_today_stats()
        if remain == 0:
            return 'Денег нет, держись'
        which_currency = {'usd': (round(remain / self.USD_RATE, 2), 'USD'),
                          'eur': (round(remain / self.EURO_RATE, 2), 'Euro'),
                          'rub': (round(remain, 2), 'руб')}[currency]
        (money_amount, currency) = which_currency
        if money_amount > 0:
            return (f'На сегодня осталось {money_amount} '
                    f'{currency}')
        else:
            return (f'Денег нет, держись: твой долг - {abs(money_amount)} '
                    f'{currency}')
 

class Record:
    def __init__(self, amount, comment, date=None):
        """Создание записей.

        Свойства экземпляров класса:
        -число amount(денежная сумма или количество килокалорий);
        -дата создания записи date(передаётся в явном виде в конструктор,
         либо присваивается значение по умолчанию — текущая дата);
        -комментарий comment (на что потрачены деньги
         или откуда взялись калории). 
        """
        
        self.amount = amount
        self.comment = comment
        if date is None:
            date = dt.datetime.now().date()
        else:
            date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.date = date
