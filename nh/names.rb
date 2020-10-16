module LastName
  LIST = File.open('data/names.csv', 'r', &:read).split(/\n/)

  def self.prefix(num = 2)
    return LIST if num <= 0

    LIST.map do |name|
      name[0..(num-1)]
    end.uniq
  end
end
